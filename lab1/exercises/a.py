from nltk.corpus import wordnet as wn

def explore_word(word):
    synsets = wn.synsets(word)
    related = {
        "synonyms": set(),
        "antonyms": set(),
        "hypernyms": set(),
        "hyponyms": set(),
        "meronyms": set(),
        "definitions": []
    }
    
    for syn in synsets:
        related["definitions"].append(syn.definition())
        for lemma in syn.lemmas():
            related["synonyms"].add(lemma.name())
            for ant in lemma.antonyms():
                related["antonyms"].add(ant.name())
        for hyper in syn.hypernyms():
            related["hypernyms"].update([l.name() for l in hyper.lemmas()])
        for hypo in syn.hyponyms():
            related["hyponyms"].update([l.name() for l in hypo.lemmas()])        
        for mero in syn.part_meronyms():
            related["meronyms"].update([l.name() for l in mero.lemmas()])
    
    return related

print(explore_word(input('Tell me a word: ')))
