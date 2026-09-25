import subprocess, random

from nlp.matcher import load_intents, load_responses, find_intent

def clear_screen():
    subprocess.run('cls', shell=True)

def main():
    clear_screen()
    intents = load_intents("data/intents.txt")
    responses = load_responses("data/responses.txt")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Indian Scammer: Goodbye, sir.")
            break
        intent, score = find_intent(user_input, intents)
        if intent in responses:
            reply = random.choice(responses[intent])
        else:
            reply = "I'm sorry, sir. I don't understand."
        print("Indian Scammer:", reply)

if __name__ == "__main__":
    main()