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

def find_intent(message, intents):
    tokens = tokenize(message)

    best_intent = None
    best_score = 0

    for intent, keywords in intents.items():
        score = 0

        for word in tokens:
            if word in keywords:
                score += 1

        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent

if __name__ == "__main__":
    intents = load_intents("data/intents.txt")

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            break

        intent = find_intent(message, intents)
        print("Intent:", intent)