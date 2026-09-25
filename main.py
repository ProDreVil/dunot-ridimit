from nlp.matcher import load_intents, find_intent

def main():
    intents = load_intents("data/intents.txt")

    print("=== ScammerBot ===")
    print("Type 'exit' to leave.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bot: Goodbye, sir.")
            break

        intent = find_intent(user_input, intents)

        print("Bot: Detected intent:", intent)


if __name__ == "__main__":
    main()