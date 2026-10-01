import subprocess, random

from nlp.matcher import *
from nlp.regex import *

def clear_screen():
    subprocess.run('cls', shell=True)

def timed_input(prompt, timeout=60):
    import msvcrt
    import time
    print(prompt, end="", flush=True)
    start_time = time.time()
    user_input = ""
    while True:
        if time.time() - start_time >= timeout:
            print()
            print("No response received for 60 seconds. Ending session.")
            return None
        if msvcrt.kbhit():
            char = msvcrt.getwch()
            if char == "\r":
                print()
                return user_input
            elif char == "\b":
                if user_input:
                    user_input = user_input[:-1]
                    print("\b \b", end="", flush=True)
            else:
                user_input += char
                print(char, end="", flush=True)

def select_response(
    money_value, money, needs_clarification, giftcard_goal, goal_just_activated, is_yes, is_no,
    is_context, intent, responses, context_responses, templates
):
    if goal_just_activated:
        reply = random.choice(responses["goal_giftcard"])
        return apply_template(reply, templates)
    if money_value is not None:
        if money_value < 100:
            reply = random.choice(responses["low_money"])
        else:
            reply = random.choice(responses["money"])
        return reply.replace("{money}", money)
    if needs_clarification:
        reply = random.choice(responses["clarify"])
    elif giftcard_goal and is_yes:
        reply = random.choice(responses["giftcard_yes"])
    elif giftcard_goal and is_no:
        reply = random.choice(responses["giftcard_no"])
    elif giftcard_goal and is_context:
        reply = random.choice(responses["goal_giftcard"])
    elif is_context and intent in context_responses:
        reply = random.choice(context_responses[intent])
    elif intent in responses:
        reply = random.choice(responses[intent])
    else:
        reply = random.choice(responses["fallback"])
    return apply_template(reply, templates)

def process_money(message):
    money = extract_money(message)
    money_value = None
    if money:
        money_value = re.search(r"\d+(?:,\d{3})*(?:\.\d+)?", money).group()
        money_value = float(money_value.replace(",", ""))
    return money, money_value

def interpret_regex(regex_intent):
    is_yes = regex_intent == "yes"
    is_no = regex_intent == "no"
    is_question = regex_intent == "question"
    return is_yes, is_no, is_question

def update_progress(progress, detected_intents, intents):
    for intent, _ in detected_intents:
        if intent in intents:
            progress += intents[intent]["progress"]
    return progress

def check_goal(progress):
    return progress >= 10

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
    print("Tech Scammer:", reply)
    while True:
        user_input = timed_input("You: ")
        if user_input is None:
            break
        regex_intent = detect_regex(user_input)
        money, money_value = process_money(user_input)
        is_yes, is_no, is_question = interpret_regex(regex_intent)
        if user_input.lower() == "exit":
            reply = random.choice(responses["goodbye"])
            reply = apply_template(reply, templates)
            print("Tech Scammer:", reply)
            break
        multi_intents = find_all_intents(user_input, intents)
        progress = update_progress(progress, multi_intents, intents)
        print(f"[DEBUG] Progress: {progress}")
        if len(multi_intents) > 1:
            goal_just_activated = progress >= 10 and not giftcard_goal
            giftcard_goal = check_goal(progress)
            for intent, score in multi_intents:
                if intent in responses:
                    reply = random.choice(responses[intent])
                    reply = apply_template(reply, templates)
                    print("Tech Scammer:", reply)
            continue
        intent, score = find_intent(user_input, intents, patterns)
        print(f"[DEBUG] Intent: {intent} | Score: {score}")
        is_context = False
        if intent == "context" and last_intent is not None:
            is_context = True
            intent = last_intent
        elif intent != "unknown":
            last_intent = intent
        if intent in intents:
            progress += intents[intent]["progress"]
        giftcard_goal = check_goal(progress)
        tokens = user_input.split()
        needs_clarification = (
            not is_question
            and intent != "unknown"
            and intent not in ["greeting", "goodbye", "help"]
            and score > 0
            and score <= 10
            and len(tokens) <= 2
        )
        reply = select_response(
            money_value=money_value,
            money=money,
            needs_clarification=needs_clarification,
            giftcard_goal=giftcard_goal,
            goal_just_activated=goal_just_activated,
            is_yes=is_yes,
            is_no=is_no,
            is_context=is_context,
            intent=intent,
            responses=responses,
            context_responses=context_responses,
            templates=templates
        )
        print("Tech Scammer:", reply)

if __name__ == "__main__":
    main()