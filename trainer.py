from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer as DefaultTrainer
from data import collate_data, BabiqaDataset
from torch.utils.data import ConcatDataset
import torch
from transformers.optimization import get_scheduler
import sys
import argparse


torch.manual_seed(42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_dir = "gpt2-babi"

def create_test_args() -> list:
    return [
        "trainer.py",
        "gpt2",
        "-task_number", "27",
        "-lr", "1e-4",
        "-epoch", "1",
        "-batch_size", "8",
        "-grouping", "True",
    ]


parser = argparse.ArgumentParser()
parser.add_argument("model_name")
parser.add_argument("-task_number", default=2, type=int)
parser.add_argument('-lr', default=3e-4, type=float)
parser.add_argument('-batch_size', default=6, type=int)
parser.add_argument('-epoch', default=3, type=int)
parser.add_argument('-ga', '--gradient_accumulation', default=1, type=int)
parser.add_argument('-grouping', default=False, type=bool)


class Trainer(DefaultTrainer):
    def create_scheduler(self,  num_training_steps: int, optimizer: torch.optim.Optimizer = None):
        """
        disable scheduler
        """
        if self.lr_scheduler is None:
            self.lr_scheduler = get_scheduler(
                self.args.lr_scheduler_type,
                optimizer=self.optimizer if optimizer is None else optimizer,
                num_warmup_steps=0,
                num_training_steps=sys.maxsize,
            )
        return self.lr_scheduler


def make_dataset(task_number, grouping=False):
    if task_number <= 0:
        if task_number < 0:
            task_number = abs(task_number)
        else: task_number = 20
        train_ds = ConcatDataset(
            [
                BabiqaDataset(tokenizer, split="train", task_no=f"qa{task_id+1}")
                for task_id in range(task_number)
            ]
        )
        test_ds = ConcatDataset(
            [
                BabiqaDataset(tokenizer, split="test", task_no=f"qa{task_id+1}")
                for task_id in range(task_number)
            ]
        )
    else:
        if grouping:
            train_ds = ConcatDataset(
                [
                    BabiqaDataset(tokenizer, split="train", task_no=f"qa{task_id}")
                    for task_id in range(26, task_number+1)
                ]
            )
            test_ds = ConcatDataset(
                [
                    BabiqaDataset(tokenizer, split="test", task_no=f"qa{task_id}")
                    for task_id in range(26, task_number+1)
                ]
            )
        else:
            train_ds = ConcatDataset([ BabiqaDataset(tokenizer, split="train", task_no=f"qa{task_number}") ])
            test_ds = ConcatDataset([ BabiqaDataset(tokenizer, split="test", task_no=f"qa{task_number}") ])

    return train_ds, test_ds


if __name__ == "__main__":
    sys.argv = create_test_args()
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    model = AutoModelForCausalLM.from_pretrained(args.model_name)
    model.to(device)

    train_dataset, test_dataset = make_dataset(args.task_number, args.grouping)

    training_args = TrainingArguments(
        output_dir=model_dir,
        save_strategy="no",
        eval_strategy="no",
        learning_rate=args.lr,
        num_train_epochs=args.epoch,
        weight_decay=0.0,
        push_to_hub=False,
        load_best_model_at_end=False,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation,
        lr_scheduler_type="constant",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        data_collator=lambda x: collate_data(
            x,
            padding_value=tokenizer.eos_token_id,
            label_padding_value=tokenizer.eos_token_id
        ),
    )

    trainer.train()
    trainer.save_model(model_dir)
    tokenizer.save_pretrained(model_dir)
