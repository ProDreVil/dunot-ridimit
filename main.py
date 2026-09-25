import subprocess, random

from nlp.matcher import *

def clear_screen():
    subprocess.run('cls', shell=True)

def main():
    clear_screen()
    intents = load_intents("data/intents.txt")
    patterns = load_patterns("data/patterns.txt")
    responses = load_responses("data/responses.txt")
    context_responses = loader("data/context.txt")
    templates = loader("data/template.txt")
    last_intent = None
    reply = random.choice(responses["greeting"])
    reply = apply_template(reply, templates)
    print("Indian Scammer:", reply)
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            reply = random.choice(responses["goodbye"])
            reply = apply_template(reply, templates)
            print("Indian Scammer:", reply)
            break
        multi_intents = find_all_intents(user_input, intents)
        if len(multi_intents) > 1:
            for intent, score in multi_intents:
                if intent in responses:
                    reply = random.choice(responses[intent])
                    reply = apply_template(reply, templates)
                    print("Indian Scammer:", reply)
            continue
        intent, score = find_intent(user_input, intents, patterns)
        is_context = False
        if intent == "context" and last_intent is not None:
            is_context = True
            intent = last_intent
        elif intent != "unknown":
            last_intent = intent
        if is_context and intent in context_responses:
            reply = random.choice(context_responses[intent])
            reply = apply_template(reply, templates)
        elif intent in responses:
            reply = random.choice(responses[intent])
            reply = apply_template(reply, templates)
        else:
            reply = random.choice(responses["fallback"])
        print("Indian Scammer:", reply)

if __name__ == "__main__":
    main()