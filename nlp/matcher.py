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
                keyword, weight = line.rsplit(":", 1)
                intents[current_intent].append((keyword.lower(), int(weight)))
    return intents

def load_patterns(filename):
    patterns = {}
    current_intent = None
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                current_intent = line[1:-1]
                patterns[current_intent] = []
            elif current_intent:
                patterns[current_intent].append(line.lower())
    return patterns

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

def load_context_responses(filename):
    return load_responses(filename)

def find_intent(message, intents, patterns):
    cleaned_message = clean_text(message)
    tokens = tokenize(message)
    for intent, phrases in patterns.items():
        for phrase in phrases:
            if phrase in cleaned_message:
                return intent, 100
    best_intent = "unknown"
    best_score = 0
    for intent, keywords in intents.items():
        score = 0
        for keyword, weight in keywords:
            if " " in keyword:
                if keyword in cleaned_message:
                    score += weight
            elif keyword in tokens:
                score += weight
        if score > best_score:
            best_score = score
            best_intent = intent
    return best_intent, best_score

def find_all_intents(message, intents):
    cleaned_message = clean_text(message)
    tokens = tokenize(message)
    matched_intents = []
    for intent, keywords in intents.items():
        score = 0
        for keyword, weight in keywords:
            if " " in keyword:
                if keyword in cleaned_message:
                    score += weight
            elif keyword in tokens:
                score += weight
        if score > 0:
            matched_intents.append((intent, score))
    matched_intents.sort(key=lambda x: x[1], reverse=True)
    return matched_intents[:2]