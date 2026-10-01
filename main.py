import subprocess, random

from nlp.matcher import *
from nlp.regex import *

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
        regex_intent = detect_regex(user_input)
        money = extract_money(user_input)
        money_value = None
        if money:
            money_value = re.search(r"\d+(?:,\d{3})*(?:\.\d+)?", money).group()
            money_value = float(money_value.replace(",", ""))
        if user_input.lower() == "exit":
            reply = random.choice(responses["goodbye"])
            reply = apply_template(reply, templates)
            print("Indian Scammer:", reply)
            break
        multi_intents = find_all_intents(user_input, intents)
        if multi_intents:
            for intent, score in multi_intents:
                if intent in intents:
                    progress += intents[intent]["progress"]
        if len(multi_intents) > 1:
            if progress >= 10:
                giftcard_goal = True
            for intent, score in multi_intents:
                if intent in responses:
                    reply = random.choice(responses[intent])
                    reply = apply_template(reply, templates)
                    print("Indian Scammer:", reply)
            continue
        multi_intent_handled = len(multi_intents) > 1
        intent, score = find_intent(user_input, intents, patterns)
        text = user_input.lower().strip()
        is_yes = regex_intent == "yes"
        is_no = regex_intent == "no"
        is_question = regex_intent == "question"
        is_context = False
        if intent == "context" and last_intent is not None:
            is_context = True
            intent = last_intent
        elif intent != "unknown":
            last_intent = intent
        if not multi_intent_handled and intent in intents:
            progress += intents[intent]["progress"]
        if progress >= 10 and not giftcard_goal:
            giftcard_goal = True
        tokens = user_input.split()
        needs_clarification = (
            not is_question
            and intent != "unknown"
            and intent not in ["greeting", "goodbye", "help"]
            and score > 0
            and score <= 10
            and len(tokens) <= 2
        )
        if money_value is not None:
            if money_value < 100:
                reply = random.choice(responses["low_money"])
            else:
                reply = random.choice(responses["money"])

            reply = reply.replace("{money}", money)
        elif needs_clarification:
            reply = random.choice(responses["clarify"])
            reply = apply_template(reply, templates)
        elif giftcard_goal and is_yes:
            reply = random.choice(responses["giftcard_yes"])
            reply = apply_template(reply, templates)
        elif giftcard_goal and is_no:
            reply = random.choice(responses["giftcard_no"])
            reply = apply_template(reply, templates)
        elif giftcard_goal and is_context:
            reply = random.choice(responses["goal_giftcard"])
            reply = apply_template(reply, templates)
        elif is_context and intent in context_responses:
            reply = random.choice(context_responses[intent])
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