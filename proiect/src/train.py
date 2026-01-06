import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from preprocess import load_task1_data, split_train_dev

# --------------------------
# SETTINGS
# --------------------------
MODEL_NAME = "distilbert-base-uncased"
MAX_LEN = 128
BATCH_SIZE = 16
EPOCHS = 5
LEARNING_RATE = 2e-5

# --------------------------
# DATASET CLASS
# --------------------------
class Task1Dataset(Dataset):
    def __init__(self, samples, tokenizer):
        self.samples = samples
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        s = self.samples[idx]
        enc = self.tokenizer(
            s["input_text"],
            truncation=True,
            padding="max_length",
            max_length=MAX_LEN,
            return_tensors="pt"
        )

        labels = torch.tensor([s["valence"], s["arousal"]], dtype=torch.float)

        return {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "labels": labels
        }

# --------------------------
# MAIN
# --------------------------
def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    paths = [
        "data/eng_laptop_train_alltasks.jsonl",
        "data/eng_restaurant_train_alltasks.jsonl"
    ]
    samples = load_task1_data(paths)
    train_samples, dev_samples = split_train_dev(samples, dev_ratio=0.1)

    train_ds = Task1Dataset(train_samples, tokenizer)
    dev_ds = Task1Dataset(dev_samples, tokenizer)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
        problem_type="regression"
    )

    args = TrainingArguments(
        output_dir="models/task1",
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        logging_steps=50,
        save_total_limit=1,
        do_train=True,
        do_eval=True,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=dev_ds
    )

    trainer.train()

    model.save_pretrained("models/task1")
    tokenizer.save_pretrained("models/task1")

if __name__ == "__main__":
    main()
