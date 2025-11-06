docs = [
    "The study of mechanical or 'formal' reasoning began with philosophers and mathematicians in antiquity. The study of logic led directly to Alan Turing's theory of computation, which suggested that a machine, by shuffling symbols as simple as '0' and '1', could simulate any conceivable form of mathematical reasoning. This, along with concurrent discoveries in cybernetics, information theory and neurobiology, led researchers to consider the possibility of building an 'electronic brain'.",
    "The field of AI research was founded at a workshop at Dartmouth College in 1956.",
    "The Lighthill report … is a scholarly article by James Lighthill, published in 1973. The report gave a very pessimistic prognosis for many core aspects of research in the field of artificial intelligence. It 'formed the basis for the decision by the British government to end support for AI research in most British universities', contributing to an AI winter in Britain.",
    "Automated art dates back at least to the automata of ancient Greek civilization, when inventors such as Daedalus and Hero of Alexandria were described as designing machines capable of writing text, generating sounds, and playing music. … In 1950, Turing's paper 'Computing Machinery and Intelligence' focused on whether machines can mimic human behavior convincingly.",
    "Artificial intelligence: a university textbook on artificial intelligence (AI), written by Patrick Henry Winston. It was first published in 1977, and the third edition of the book was released in 1992.",
    "Climate change refers to long-term shifts in temperatures and weather patterns. Such shifts can be natural, due to changes in the sun's activity or large volcanic eruptions. But since the 1800s, human activities have been the main driver of climate change, primarily due to the burning of fossil fuels like coal, oil and gas.",
    "The atmosphere is a dynamic fluid that is continually in motion. Both its physical properties and its rate and direction of motion are influenced by a variety of factors, including solar radiation, the geographic position of continents, ocean currents, the location and orientation of mountain ranges, atmospheric chemistry, and vegetation growing on the land surface. Climate is often defined loosely as the average weather at a particular place, incorporating such features as temperature, precipitation, humidity, and windiness.",
    "Burning fossil fuels generates greenhouse gas emissions that act like a blanket wrapped around the Earth, trapping the sun's heat and raising temperatures. The main greenhouse gases that are causing climate change include carbon dioxide and methane. These come from using gasoline for driving a car or coal for heating a building, for example.",
    "Undoubtedly, people have always been aware of climatic variation at the relatively short timescales of seasons, years, and decades. Naturalists of this time, including Scottish geologist James Croll, Swiss-born naturalist and geologist Louis Agassiz, English naturalist Charles Darwin, American botanist Asa Gray, and Welsh naturalist Alfred Russel Wallace, came to recognize geologic and biogeographic evidence that made sense only in the light of past climates radically different from those prevailing today.",
    "The atmosphere is linked to other features of Earth, including oceans, ice masses (glaciers and sea-ice), land surfaces, and vegetation. Together, they make up an integrated Earth system, in which all components interact and influence one another in often complex ways. For instance, climate influences the distribution of vegetation on Earth's surface, but vegetation in turn influences climate by reflecting radiant energy back into the atmosphere.",
    "Jazz music, which was developed by African Americans and was influenced by both African rhythms and European harmonic structure, first appeared at the turn of the 20th century and has since undergone several distinctive phases of development.",
    "Jazz, musical form, often improvisational, developed by African Americans and influenced by both European harmonic structure and African rhythms. Though its specific origins are not known, the music developed principally as an amalgam in the late 19th- and early-20th-century musical culture of New Orleans.",
    "Jazz is characterized by syncopated rhythms, polyphonic ensemble playing, varying degrees of improvisation, often deliberate deviations of pitch, and the use of original timbres.",
    "The sounds that jazz musicians make on their instruments—the way they attack, inflect, release, embellish, and colour notes—characterize jazz playing to such an extent that if a classical piece were played by jazz musicians in their idiomatic phrasings, it would in all likelihood be called jazz.",
    "Most early classical composers were drawn to its instrumental sounds and timbres, the unusual effects and inflections of jazz playing (brass mutes, glissandos, scoops, bends, and stringless ensembles). Indeed, the sounds that jazz musicians make characterize jazz playing to such an extent."
]

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# ex 1, lemmatization and stopword removal + BoW and TF-IDF
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return ' '.join(tokens)

preprocessed_docs = [preprocess(doc) for doc in docs]

from sklearn.feature_extraction.text import CountVectorizer

print("\n \n ex. 1: Use text preprocessing techniques (stemming/lematization, stop words removal) and create the bag-of-words and TF-IDF vectorizations \n")
bow_vectorizer = CountVectorizer()
bow = bow_vectorizer.fit_transform(preprocessed_docs)
print("\nBag-of-Words shape:", bow.shape)
print("\nFeature names:", bow_vectorizer.get_feature_names_out())

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(preprocessed_docs)

print("\nTF-IDF shape:", tfidf.shape)
print("\nFeature names:", tfidf_vectorizer.get_feature_names_out())

# ex 2 Latent Semantic Analysis (LSA) with SVD

from sklearn.decomposition import TruncatedSVD
n_components = 2
# n_components = 5
print("\n ex. 2: Use Latent Semantic Analysis with SVD for \n a. the bag-of-words encoding and  \n b. the TF-IDF encoding  \n")


# lsa bow 
svd_bow = TruncatedSVD(n_components=n_components, random_state=42)
lsa_bow = svd_bow.fit_transform(bow)

print("LSA (BoW) shape:", lsa_bow.shape)
print("Explained variance ratio:", svd_bow.explained_variance_ratio_)


# lsa tfidf
svd_tfidf = TruncatedSVD(n_components=n_components, random_state=42)
lsa_tfidf = svd_tfidf.fit_transform(tfidf)

print("LSA (TF-IDF) shape:", lsa_tfidf.shape)
print("Explained variance ratio:", svd_tfidf.explained_variance_ratio_)

# ex 3 Use non-negative matrix factorization 

print("\n ex. 3 Use Non-negative matrix factorization \n")

from sklearn.decomposition import NMF

n_topics = 3  # you can choose 2,3,5 depending on how many latent topics you want

# NMF on BoW
nmf_bow = NMF(n_components=n_topics, random_state=42)
W_bow = nmf_bow.fit_transform(bow)  # document-topic matrix
H_bow = nmf_bow.components_         # topic-word matrix

print("NMF (BoW) W shape:", W_bow.shape)
print("NMF (BoW) H shape:", H_bow.shape)

# NMF on TF-IDF
nmf_tfidf = NMF(n_components=n_topics, random_state=42)
W_tfidf = nmf_tfidf.fit_transform(tfidf)
H_tfidf = nmf_tfidf.components_

print("NMF (TF-IDF) W shape:", W_tfidf.shape)
print("NMF (TF-IDF) H shape:", H_tfidf.shape)


print("\n ex. 4 Use LDA \n")

from sklearn.decomposition import LatentDirichletAllocation

n_topics = 3  
lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
lda_matrix = lda.fit_transform(bow)  

print("LDA document-topic matrix shape:", lda_matrix.shape)

vocab = bow_vectorizer.get_feature_names_out()  # from CountVectorizer
n_top_words = 5

for topic_idx, topic in enumerate(lda.components_):
    top_words = [vocab[i] for i in topic.argsort()[-n_top_words:][::-1]]
    print(f"Topic {topic_idx+1}: {', '.join(top_words)}")

print("\n ex. 5 Document on the evaluation metrics from the gensim library and apply them on ypu results \n")

# from gensim.utils import simple_preprocess

# tokenized_docs = [simple_preprocess(doc) for doc in docs]

# from gensim.corpora import Dictionary

# dictionary = Dictionary(tokenized_docs)
# corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

# from gensim.models import LdaModel
# from gensim.models.coherencemodel import CoherenceModel


# lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=3, random_state=42, passes=10)


# coherence_model_lda = CoherenceModel(model=lda_model, texts=tokenized_docs, dictionary=dictionary, coherence='c_v')
# coherence_lda = coherence_model_lda.get_coherence()
# print("LDA Coherence Score:", coherence_lda)

