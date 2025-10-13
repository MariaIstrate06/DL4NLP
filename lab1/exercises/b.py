import random
from nltk.corpus import wordnet as wn

def similarity_score(word1, word2):
    syn1 = wn.synsets(word1)
    syn2 = wn.synsets(word2)
    
    if not syn1 or not syn2:
        return 0
    s1, s2 = syn1[0], syn2[0]
    
    sim = s1.wup_similarity(s2) 
    return sim if sim else 0

def word_association_game():
    words = ["human", "dog", "cat", "university", "tree"]
    original = random.choice(words)
    print(f"\nYour word is: {original}")
    
    user_word = input("Enter a related word: ").strip()
    score = similarity_score(original, user_word)
    points = int(score * 100) if score > 0 else 0
    
    if points > 70:
        feedback = "YEY"
    elif points > 40:
        feedback = "good-ish"
    elif points > 10:
        feedback = "mmm..."
    else:
        feedback = "not really :("
    
    print(f"Your word: {user_word}")
    print(f"Similarity score: {score:.2f}: {points} points")
    print(f"Feedback: {feedback}\n")

word_association_game()
