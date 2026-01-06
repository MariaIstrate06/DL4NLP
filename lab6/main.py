# --- INSTALL DEPENDENCIES (run once) ---
# pip install gensim matplotlib scikit-learn

# --- IMPORTS ---
import gensim.downloader as api
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from sklearn.decomposition import PCA

# --- SETUP ---

# === LOAD GloVe (50 dimensions) ===
# Download from: https://nlp.stanford.edu/projects/glove/
# File used: glove.6B.50d.txt
# You’ll need to put it in the same folder as this script.

glove_input_file = 'glove.6B.50d.txt'
word2vec_output_file = 'glove.6B.50d.word2vec.txt'

# Convert GloVe format → word2vec format (only once)
glove2word2vec(glove_input_file, word2vec_output_file)

# Load model
glove_model = KeyedVectors.load_word2vec_format(word2vec_output_file, binary=False)
print("✅ GloVe loaded successfully!")

# === LOAD Word2Vec ===
# Using a smaller pretrained version from gensim to avoid the massive 3GB GoogleNews file
word2vec_model = api.load("word2vec-google-news-300")
print("✅ Word2Vec loaded successfully!")

# --- CHOOSE 20 WORDS ---
words = [
    'king', 'queen', 'man', 'woman', 'dog', 'cat', 'apple', 'orange',
    'car', 'bus', 'music', 'art', 'happy', 'sad', 'big', 'small',
    'love', 'hate', 'sun', 'moon'
]

# Ensure all chosen words exist in both vocabularies
words = [w for w in words if w in glove_model.key_to_index and w in word2vec_model.key_to_index]
print(f"✅ Using {len(words)} words: {words}")

# --- RANDOM DIMENSIONS ---
dims_glove = random.sample(range(glove_model.vector_size), 3)
dims_w2v = random.sample(range(word2vec_model.vector_size), 3)
print("🎲 Random GloVe dims:", dims_glove)
print("🎲 Random Word2Vec dims:", dims_w2v)

# --- 3D PLOT FUNCTION ---
def plot_3d(words, vectors, dims, title):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(vectors[:, 0], vectors[:, 1], vectors[:, 2])

    for i, word in enumerate(words):
        ax.text(vectors[i, 0], vectors[i, 1], vectors[i, 2], word)

    ax.set_xlabel(f"dim {dims[0]}")
    ax.set_ylabel(f"dim {dims[1]}")
    ax.set_zlabel(f"dim {dims[2]}")
    plt.title(title)
    plt.show()

# --- GloVe VISUALIZATION ---
vectors_glove = np.array([glove_model[w][dims_glove] for w in words])
plot_3d(words, vectors_glove, dims_glove, "GloVe 3D Visualization (random dimensions)")

# --- Word2Vec VISUALIZATION ---
vectors_w2v = np.array([word2vec_model[w][dims_w2v] for w in words])
plot_3d(words, vectors_w2v, dims_w2v, "Word2Vec 3D Visualization (random dimensions)")

# --- BONUS: PCA REDUCTION (meaningful visualization) ---
def plot_pca(model, words, title):
    vectors_full = np.array([model[w] for w in words])
    pca = PCA(n_components=3)
    vectors_pca = pca.fit_transform(vectors_full)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(vectors_pca[:, 0], vectors_pca[:, 1], vectors_pca[:, 2])

    for i, word in enumerate(words):
        ax.text(vectors_pca[i, 0], vectors_pca[i, 1], vectors_pca[i, 2], word)

    plt.title(title + " (PCA)")
    plt.show()

plot_pca(glove_model, words, "GloVe PCA Visualization")
plot_pca(word2vec_model, words, "Word2Vec PCA Visualization")
