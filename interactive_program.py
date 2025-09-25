while True:
    text = input("say something: ")
    print(f"you said: {text}")
    if text == "exit":
        break
    elif text.startswith("exec: "):
        print(f"executing: {text[6:]}")
        exec(text[6:])
print("bye bye!")
