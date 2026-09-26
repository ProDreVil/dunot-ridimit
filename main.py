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
    progress = 0
    giftcard_goal = False
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
        if multi_intents:
            progress += 1
        if len(multi_intents) > 1:
            if progress >= 3:
                giftcard_goal = True
            for intent, score in multi_intents:
                if intent in responses:
                    reply = random.choice(responses[intent])
                    reply = apply_template(reply, templates)
                    print("Indian Scammer:", reply)
            continue
        multi_intent_handled = len(multi_intents) > 1
        intent, score = find_intent(user_input, intents, patterns)
        is_context = False
        if intent == "context" and last_intent is not None:
            is_context = True
            intent = last_intent
        elif intent != "unknown":
            last_intent = intent
        if not multi_intent_handled and intent not in ["unknown", "greeting", "goodbye"]:
            progress += 1
        if progress >= 3:
            giftcard_goal = True
        tokens = user_input.split()
        needs_clarification = (
            intent != "unknown"
            and intent not in ["greeting", "goodbye", "help"]
            and score > 0
            and score <= 3
            and len(tokens) <= 2
        )
        if needs_clarification:
            reply = random.choice(responses["clarify"])
            reply = apply_template(reply, templates)
        elif is_context and intent in context_responses:
            reply = random.choice(context_responses[intent])
            reply = apply_template(reply, templates)
        elif giftcard_goal and intent == "help":
            reply = random.choice(responses["goal_giftcard"])
            reply = apply_template(reply, templates)
        elif intent in responses:
            reply = random.choice(responses[intent])
            reply = apply_template(reply, templates)
        else:
            reply = random.choice(responses["fallback"])
            reply = apply_template(reply, templates)
        print("Indian Scammer:", reply)

if __name__ == "__main__":
    main()