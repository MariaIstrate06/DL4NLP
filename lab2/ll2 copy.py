from collections import defaultdict, Counter

corpus = [
    "there is a big house",
    "i buy a house",
    "they buy the new house",
]

def get_vocab(corpus):
    vocab = set()
    for sentence in corpus:
        tokens = list(sentence.lower())
        vocab = vocab.union(tokens)
    return vocab

def get_pairs(vocab: set, corpus):
    pairs = dict()
    v = list(vocab)
    v.sort(key=lambda word: len(word))
    print(v)
    idx = 0
    for s in corpus:
        while idx < len(s):
            for tok in v:
                if s[idx:idx+len(tok)] == tok:



def get_pairs(vocab: set, corpus):
    pairs = dict()
    l = list(vocab)
    for widx1 in range(0, len(l)):
        for widx2 in range(widx1+1, len(l)):
            pair = (l[widx1], l[widx2])
            if pair in pairs:
                continue
            freq = sum([sentence.count(l[widx1] + l[widx2]) for sentence in corpus])
            pairs[pair] = freq
    return pairs

def merge_vocab(pair, vocab:set):
    print(pair)
    vocab.remove(pair[0])
    vocab.remove(pair[1])
    vocab.add((pair[0] + pair[1]))
    return vocab

vocab = get_vocab(corpus)

num_merges = 10
for i in range(num_merges):
    pairs = get_pairs(vocab, corpus)
    print(i, pairs)
    if not pairs:
        break
    best = max(pairs, key=pairs.get)
    print('============================')
    print(pairs)
    print('best;', best)
    vocab = merge_vocab(best, vocab)
    print(f"Merge {i+1}: {best}")

print("\nFinal vocabulary:")
for word in vocab:
    print(word)