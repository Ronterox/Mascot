from nomic.gpt4all import GPT4All

m = GPT4All('gpt4all-lora-unfiltered-quantized')

CONTEXT_LIMIT = 20
isOpened = False
currentContext = 0

def predict(prompt):
    global isOpened, currentContext

    if not isOpened:
        isOpened = True
        m.open()

    print(f"Prompt: {prompt}\n")
    prediction = m.prompt(prompt, True)
    currentContext += 1
    print(f"\nCurrent context: {currentContext}")

    if currentContext > CONTEXT_LIMIT:
        m.close()
        isOpened = False
        currentContext = 0

    return prediction

if __name__ == "__main__":
    predict("Is this a positive comment. I HATE MINECRAFT!")
    predict("Write short essay about why you hate minecraft.")