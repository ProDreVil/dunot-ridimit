import subprocess, random

from nlp.matcher import load_intents, load_patterns, load_responses, find_intent

def clear_screen():
    subprocess.run('cls', shell=True)

def main():
    clear_screen()
    intents = load_intents("data/intents.txt")
    patterns = load_patterns("data/patterns.txt")
    responses = load_responses("data/responses.txt")
    last_intent = None
    reply = random.choice(responses["greeting"])
    print("Indian Scammer:", reply)
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Indian Scammer: Goodbye, sir.")
            break
        intent, score = find_intent(user_input, intents, patterns)
        if intent == "context" and last_intent is not None:
            intent = last_intent
        elif intent != "unknown":
            last_intent = intent
        if intent in responses:
            reply = random.choice(responses[intent])
        else:
            reply = random.choice(responses["fallback"])
        print("Indian Scammer:", reply)

if __name__ == "__main__":
    main()