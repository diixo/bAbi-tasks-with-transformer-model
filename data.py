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


def get_next_qa(dataset):
    for x in dataset:
        story = x.get('story', None)
        if story:
            sentences = story.get("text",  None)
            sent_types = story.get("type", [])
            
            context = ""
            for s_idx, sent in enumerate(sentences):
                if sent_types[s_idx] == 1:
                    question = sent
                    answer = story["answer"][s_idx]
                    context = context.strip()
                    yield context, question, answer
                else:
                    context += f"{sent}\n"


class BabiqaDataset():

    def __init__(self,tokenizer, task_no="qa1", split="train", no_answer=False) -> None:
        self.tokenizer:PreTrainedTokenizer = tokenizer
        dataset = load_dataset('babi_qa', type='en', task_no=task_no)[split]
        self.data = list(get_next_qa(dataset))
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
        enc_input = self.tokenizer(
            input_text, truncation=True, add_special_tokens=False, max_length=1000, return_tensors="pt"
            )["input_ids"]

        # train in Supervised fine-tuning mode:
        if self.no_answer:
            input_ids = enc_input
        else:
            enc_output = self.tokenizer(
                answer, truncation=True, add_special_tokens=False, max_length=1000, return_tensors="pt"
                )["input_ids"]

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
