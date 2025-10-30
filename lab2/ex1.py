from collections import Counter, defaultdict
import re

# example corpus
corpus = [
    "sunt fericit",
    "sunt trist",
    "sunt obosit",
    "fericit sunt"
]

# preprocess sentences
def preprocess(sentences):
    return [" ".join(list(sentence)) + " </w>" for sentence in sentences]  # add word-end token

tokens = preprocess(corpus)
vocab = Counter(tokens)
print("Initial vocab:", vocab)

# BPE merges
def get_stats(vocab):
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[(symbols[i], symbols[i+1])] += freq
    return pairs

def merge_vocab(pair, vocab):
    new_vocab = {}
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    for word in vocab:
        new_word = re.sub(r'\b' + re.escape(bigram) + r'\b', replacement, word)
        new_vocab[new_word] = vocab[word]
    return new_vocab

# example: do 10 merges
num_merges = 10
for i in range(num_merges):
    pairs = get_stats(vocab)
    if not pairs:
        break
    best = max(pairs, key=pairs.get)
    vocab = merge_vocab(best, vocab)
    print(f"Merge {i+1}: {best}")
    print(vocab)
