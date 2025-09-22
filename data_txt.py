from datasets import load_dataset   
from transformers import PreTrainedTokenizer
from torch.nn.utils.rnn import pad_sequence
from collections import defaultdict
import torch


INPUT_TEMPLATE = """
Context:
{context}

Question:
{question}

Answer:
"""


def load_babi_txt(file_path: str) -> list:
    """
    Split bAbI txt specified file and return list of episodes:
    [{'story': ..., 'question': ..., 'answer': ...}, ...]
    """
    examples = []
    story_lines = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # remove sentence number
            idx, text = line.split(' ', 1)
            idx = int(idx)

            if '\t' in text:  # check marker of question line
                question, answer, _ = text.split('\t')
                # construct prompt: whole history before question
                story = ' '.join(story_lines)
                examples.append({
                    'story': story,
                    'question': question,
                    'answer': answer
                })
            else:
                story_lines.append(text)

            # reset history by new episode (new marker == 1)
            if idx == 1:
                story_lines = [text]
    return examples


class BabiqaText():

    def __init__(self, tokenizer, filepath, no_answer=False) -> None:

        self.data = load_babi_txt(filepath)
        self.tokenizer = tokenizer
        self.no_answer = no_answer


    def get_raw_item(self, index):
        context, question, answer = self.data[index]
        return {
            "context": context,
            "question": question,
            "answer": answer
        }


    def __getitem__(self, index):
        context, question, answer = self.data[index]
        cqa = {
            "context": context,
            "question": question,
            "answer": answer
        }

        if self.no_answer:
            cqa["answer"] = ""

        input_text = INPUT_TEMPLATE.format_map(cqa).strip() + "\n"
        enc_input = self.tokenizer(input_text, truncation=True, add_special_tokens=False, return_tensors="pt")["input_ids"]

        # train in Supervised fine-tuning mode:
        if self.no_answer:
            input_ids = enc_input
        else:
            enc_output = self.tokenizer(answer, truncation=True, add_special_tokens=False, return_tensors="pt")["input_ids"]

            # combine into one sequence
            input_ids = torch.cat([
                enc_input,                                                      # (1, N)
                enc_output,                                                     # (1, M)
                torch.tensor([[self.tokenizer.eos_token_id]], dtype=torch.long) # (1, 1)
            ], dim=1)                                                           # (1, N+M+1)=shape([0],[1])

        # create new array
        labels = input_ids.clone()

        # masked only input_text:   [0, :N=enc_input(1, N)]
        labels[0, :enc_input.size(1)] = -100

        batch_max_length = max(len(item)+1 for item in input_ids)
        assert batch_max_length <= 1024, f"batch_max_length={batch_max_length}<=1024: out of range"

        return {
            "input_ids": input_ids,
            "labels": labels,
        }
    
    def __len__(self):
        return len(self.data)


def collate_data(batch, padding_value, label_padding_value=-100):
    new_batch = defaultdict(lambda:[])
    for x in batch:
        for x_key in x.keys():
            new_batch[x_key].append(x[x_key][0])
    
    new_batch = dict(new_batch)
    for batch_key in new_batch.keys():
        if batch_key == "labels":
            new_batch[batch_key] = pad_sequence(new_batch[batch_key], batch_first=True, padding_value=label_padding_value)
        else:
            new_batch[batch_key] = pad_sequence(new_batch[batch_key], batch_first=True, padding_value=padding_value)

    if "input_ids" in new_batch:
        new_batch["attention_mask"] = (new_batch["input_ids"] != padding_value).long()

    return new_batch


if __name__ == "__main__":

    babi = BabiqaText(None, "datasets/dataset.txt")
    print(len(babi))
    print(babi[0])
