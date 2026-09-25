from nlp.preprocess import clean_text

def tokenize(text):
    return clean_text(text).split()