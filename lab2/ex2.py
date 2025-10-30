import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from nltk.util import ngrams


url = "https://ro.wikipedia.org/wiki/Inteligenta_artificiala"
# html = requests.get(url).text
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, 'html.parser')
# text = soup.get_text()

content_div = soup.find("div", class_="mw-parser-output")

if content_div:
    text = content_div.get_text(separator=" ", strip=True)
else:
    text = "Class not found."

tokens = re.findall(r'\b\w+\b', text.lower(), flags=re.UNICODE)
tokens = tokens[:1000]  
print("First 50 tokens:", tokens[:50])


n = 3 
trigrams = list(ngrams(tokens, n))
bigrams = list(ngrams(tokens, n-1))

trigram_counts = Counter(trigrams)
bigram_counts = Counter(bigrams)
unigram_counts = Counter(tokens)
V = len(unigram_counts)  


def trigram_prob(trigram):
    prefix = trigram[:-1]
    word = trigram[-1]
    prefix_count = bigram_counts[prefix] if prefix in bigram_counts else 0
    return (trigram_counts[trigram] + 1) / (prefix_count + V)

# test example
example = ("inteligenta", "artificiala", "este")
print(f"P({example[-1]} | {example[:-1]}) =", trigram_prob(example), '\n')


def sentence_prob(sentence_tokens):
    # add start tokens
    padded_tokens = ["<s>"]*(n-1) + sentence_tokens + ["</s>"]
    prob = 1.0
    for tri in ngrams(padded_tokens, n):
        prob *= trigram_prob(tri)
    return prob


new_sentence = ["inteligenta", "artificiala", "ajuta", "oamenii"]
print("Sentence probability:", sentence_prob(new_sentence))


from collections import defaultdict
def bpe(corpus, merges=10):
    vocab = Counter([" ".join(list(word)) + " </w>" for word in corpus])
    
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

    for i in range(merges):
        pairs = get_stats(vocab)
        if not pairs:
            break
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)
    return vocab

bpe_vocab = bpe(tokens[:50], merges=20)
print("BPE vocab example:", list(bpe_vocab.keys())[:10])


##### ex 3

new_sentence_input = input("Enter a Romanian sentence: ")

new_sentence_tokens = re.findall(r'\b\w+\b', new_sentence_input.lower(), flags=re.UNICODE)

prob = sentence_prob(new_sentence_tokens)

print(f"Sentence probability: {prob}")
