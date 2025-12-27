
import json
import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence
from transformers import PreTrainedTokenizer, GPT2TokenizerFast

ROLE_ORDER = [
    "Subject", "Object", "Recipient", "Source", "Destination", "Location", "Time"
]

INPUT_TEMPLATE_SRL = (
    "### CONTEXT:\n{context}\n"
    "### TASK: ROLES\n"
    "### OUTPUT:\n"
)


def format_srl_output_textual(srl_events):
    """Преобразуем список событий в текстовый блок ответа."""
    blocks = []
    for ev in srl_events:
        lines = ['EVENT:']
        # обязательный предикат
        pred = ev.get("predicate", "").strip()
        lines.append(f'  Predicate: "{pred}"')
        # роли в фиксированном порядке; печатаем только существующие
        for role in ROLE_ORDER:
            if role in ev:
                val = ev[role].strip()
                lines.append(f'  {role}: "{val}"')
        blocks.append("\n".join(lines))
    # пустой ответ допустим (если нет разметки) — модель должна печатать ничего
    return ("\n".join(blocks) + ("\n" if blocks else ""))


class SRLDataset(Dataset):
    def __init__(self, records, tokenizer, max_length=1024, add_eos=True, reserve_for_answer=128):
        self.data = records
        self.tok = tokenizer
        self.max_length = max_length
        self.add_eos = add_eos
        self.reserve_for_answer = reserve_for_answer

        # GPT-2 обычно без pad → паддим eos
        if self.tok.pad_token_id is None:
            if self.tok.eos_token is None:
                self.tok.add_special_tokens({"eos_token": ""})
            self.tok.pad_token = self.tok.eos_token

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        rec = self.data[idx]
        context = rec["context"]
        srl_events = rec.get("srl", []) or []

        prompt_text = INPUT_TEMPLATE_SRL.format(context=context)
        answer_text = format_srl_output_textual(srl_events)

        print(answer_text)

        # 1) Токенизируем промпт с резервом под ответ
        max_prompt = max(16, self.max_length - self.reserve_for_answer)
        enc_prompt = self.tok(
            prompt_text,
            truncation=True, add_special_tokens=False,
            max_length=max_prompt,
            return_tensors="pt",
        )["input_ids"][0]  # 1D

        # 2) Токенизируем ответ
        max_ans = self.max_length - enc_prompt.size(0) - (1 if self.add_eos else 0)
        if max_ans < 0:
            # промпт переполнил seq len — жестко усечем промпт
            enc_prompt = enc_prompt[: max(0, self.max_length - (1 if self.add_eos else 0))]
            max_ans = self.max_length - enc_prompt.size(0) - (1 if self.add_eos else 0)

        ans_ids = self.tok(
            answer_text,
            truncation=True, add_special_tokens=False,
            max_length=max_ans,
            return_tensors="pt",
        )["input_ids"][0]  # 1D

        # 3) EOS (опционально)
        eos = torch.tensor([self.tok.eos_token_id], dtype=torch.long) if self.add_eos else torch.tensor([], dtype=torch.long)

        # 4) Склейка
        input_ids = torch.cat([enc_prompt, ans_ids, eos], dim=0)
        if input_ids.size(0) > self.max_length:
            input_ids = input_ids[: self.max_length]

        # 5) labels = копия с маской на промпт (лосс только на ответе и EOS)
        labels = input_ids.clone()
        prompt_len = min(enc_prompt.size(0), labels.size(0))
        labels[:prompt_len] = -100

        return {
            "input_ids": input_ids,  # (T,)
            "labels": labels,        # (T,)
        }

def srl_collate_fn(batch, pad_id):
    input_ids = pad_sequence([b["input_ids"] for b in batch], batch_first=True, padding_value=pad_id)
    labels    = pad_sequence([b["labels"]    for b in batch], batch_first=True, padding_value=-100)
    attention_mask = (input_ids != pad_id).long()
    return {"input_ids": input_ids, "labels": labels, "attention_mask": attention_mask}


from torch.utils.data import DataLoader

# загрузка JSONL
def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

records = load_jsonl("srl.jsonl")

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
dataset = SRLDataset(records, tokenizer, max_length=1024, add_eos=True, reserve_for_answer=128)

tokenizer.padding_side = "right"
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token

loader = DataLoader(
    dataset,
    batch_size=8,
    shuffle=True,
    collate_fn=lambda b: srl_collate_fn(b, tokenizer.pad_token_id),
)

loader_iter = iter(loader)
batch = next(loader_iter)
