import json
import glob
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# --------------------------
# SETTINGS
# --------------------------
MODEL_DIR = "models/task1"
TEST_GLOB = "data/*_dev_task3.jsonl"  # will pick up all dev_task3 files
OUTPUT_FILE = "predictions_task1.jsonl"
MAX_LEN = 128
BATCH_SIZE = 16

# --------------------------
# DATASET
# --------------------------
class Task1TestDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        text = item.get("Text", "")
        quad = item.get("Quadruplet", [])
        aspect = quad[0].get("Aspect", "") if quad else ""

        enc = self.tokenizer(
            f"{text} [SEP] {aspect}",
            truncation=True,
            padding="max_length",
            max_length=MAX_LEN,
            return_tensors="pt"
        )

        return {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "id": item.get("ID", f"sample_{idx}")
        }

# --------------------------
# LOAD TEST DATA
# --------------------------
def load_test_data(glob_pattern):
    data = []
    files = glob.glob(glob_pattern)
    if not files:
        raise FileNotFoundError(f"No files found for pattern: {glob_pattern}")
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                data.append(json.loads(line))
    return data

# --------------------------
# MAIN
# --------------------------
def main():
    # 1️⃣ tokenizer + model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device)

    # 2️⃣ load all test files
    test_data = load_test_data(TEST_GLOB)
    test_ds = Task1TestDataset(test_data, tokenizer)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE)

    # 3️⃣ make predictions
    results = []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            preds = outputs.logits.cpu().numpy()  # shape: [batch, 2] -> valence, arousal

            for i, pred in enumerate(preds):
                results.append({
                    "ID": batch["id"][i],
                    "Valence": float(pred[0]),
                    "Arousal": float(pred[1])
                })

    # 4️⃣ save predictions
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(f"Predictions saved to {OUTPUT_FILE}, total samples: {len(results)}")

if __name__ == "__main__":
    main()
