import json
import random

def load_task1_data(paths):
    """
    paths: can be a single path (str) or a list of paths
    returns: flattened list of dicts with 'input_text', 'valence', 'arousal'
    """
    # make it a list if single string
    if isinstance(paths, str):
        paths = [paths]

    samples = []

    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                text = obj["Text"]

                for quad in obj.get("Quadruplet", []):
                    aspect = quad["Aspect"]
                    va = quad["VA"]
                    valence, arousal = map(float, va.split("#"))

                    samples.append({
                        "input_text": f"{text} [SEP] {aspect}",
                        "valence": valence,
                        "arousal": arousal
                    })

    return samples

def split_train_dev(samples, dev_ratio=0.1, seed=42):
    random.seed(seed)
    random.shuffle(samples)
    n_dev = int(len(samples) * dev_ratio)
    dev_samples = samples[:n_dev]
    train_samples = samples[n_dev:]
    return train_samples, dev_samples
