sentences = [
    'Flying planes can be dangerous.',
    'The parents of the bride and the groom were flying.',
    'The groom loves dangerous planes more than the bride.',
]
sentences = [s.lower() for s in sentences]
## Ex 1
cfg_grammar = """
SENTENCE -> SENT Punctuation
SENT -> S P | S P COMP
S -> Adj Noun | Pre Noun | S Pos S | S Conj S
P -> Verb | Verb S | P Adj | AuxV Verb | Verb Adj
COMP -> Comp S
Pre -> 'the'
Pos -> 'of'
Conj -> 'and'
Noun -> 'planes' | 'parents' | 'groom' | 'bride'
Adj -> 'flying' | 'dangerous'
Comp -> 'more' 'than'
Verb -> 'be' | 'loves' | 'flying' | 'were'
AuxV -> 'can'
Punctuation -> '.'
"""


def ex2(sentences, grammar_str):
    import nltk
    from nltk import CFG
    grammar_nltk = CFG.fromstring(grammar_str)
    parser = nltk.ChartParser(grammar_nltk)

    print("Phrase Structure Trees:\n")
    for i, sentence in enumerate(sentences, 1):
        tokens = nltk.word_tokenize(sentence)
        print("-" * 80)
        print(f"Sentence {i}: {sentence}")
        try:
            trees = list(parser.parse(tokens))
            if trees:
                for tree in trees:
                    print(tree)
            else:
                print("No parse tree found with the given grammar.")
        except ValueError as e:
            print(f"Parsing error: {e}")


def ex3(sentences):
    import spacy
    nlp = spacy.load("en_core_web_sm")

    print("Dependency Parsing Results:\n")
    for i, sentence in enumerate(sentences, 1):
        doc = nlp(sentence)
        print("-" * 80)
        print(f"Sentence {i}: {sentence}")
        for token in doc:
            print(f"{token.text:15} {token.dep_:15} {token.head.text:15} {token.pos_}")


ex2(sentences, cfg_grammar)
print("=" * 80)
ex3(sentences)
print("=" * 80)

"""
Ex 4

An application which needs syntactic and dependency parsing could be a Fuzzy attribute search or Extracting information from huge texts. Huge texts could include historical document collections (or wiki sites containing lore of fictional worlds).

Syntactic parsing is required for dependency parsing, but syntax alone could give additional insight into how a language changed over time, considering the kinds of words which are most frequently used or sentence structure. It could also determine the first written occurances of some idioms.

Dependency parsing could be useful in finding most frequent associations between entities, to gather informative descriptions or to build a network of related individuals or concepts. Those statistics could be binned by source, in order to get a view of all conflicting reports for a better understanding of historical events. A frequency analysis of word relations over time could also give interesting information, or could be used to determine the lineage of an idiom by doing a search over terms with the same or similar associations.
"""