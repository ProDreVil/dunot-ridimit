from nlp.preprocess import clean_text
from nlp.tokenizer import tokenize

def load_intents(filename):
    intents = {}
    current_intent = None
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                current_intent = line[1:-1]
                intents[current_intent] = []
            elif current_intent:
                intents[current_intent].append(line.lower())
    return intents

def load_responses(filename):
    responses = {}
    current_intent = None
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                current_intent = line[1:-1]
                responses[current_intent] = []
            elif current_intent:
                responses[current_intent].append(line)
    return responses

def find_intent(message, intents):
    cleaned_message = clean_text(message)
    tokens = tokenize(message)
    best_intent = "unknown"
    best_score = 0
    for intent, keywords in intents.items():
        score = 0
        for keyword in keywords:
            if " " in keyword:
                if keyword in cleaned_message:
                    score += 1
            elif keyword in tokens:
                score += 1
        if score > best_score:
            best_score = score
            best_intent = intent
    return best_intent, best_score