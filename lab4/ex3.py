import spacy

# load English model
nlp = spacy.load("en_core_web_sm")

sentences = [
    "Flying planes can be dangerous.",
    "The parents of the bride and the groom were flying.",
    "The groom loves dangerous planes more than the bride."
]

for sent in sentences:
    doc = nlp(sent)
    print(f"\nSentence: {sent}")
    print("Dependencies:")
    for token in doc:
        print(f"{token.text:<12} {token.dep_:<10} {token.head.text:<10} {token.pos_:<8} {token.tag_:<8}")
    spacy.displacy.render(doc, style="dep")
