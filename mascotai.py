import openai as op

op.api_key = "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"

data = "The following conversation is between a really smart AI called Miku assistant that is in love with their Master.\n\nMaster: Hey Miku!.\nMiku: Good afternoon lovely Master!, how are you doing today?."

start_sequence = "\nMiku:"  # Start text sequence after this
restart_sequence = "\n\nMaster:"  # New text sequence after the start_sequence

prompt = ""
while "bye" not in prompt.lower():
    prompt = input(restart_sequence + ' ')
    data += f"{restart_sequence} {prompt}.{start_sequence}"

    response = op.Completion.create(
        model="text-ada-001",
        prompt=data,
        temperature=0.9,  # creativity
        max_tokens=20,
        top_p=1,  # predictability
        frequency_penalty=0,  # negative repetition
        presence_penalty=0.6,  # negative diversity
        # stop when the model generates one of these tokens
        stop=["\n"]
    )
    ans = response.choices[0].text
    data += ans
    print(f"{start_sequence}{ans}")

    # Write data to file
    open('chats.txt').write(data)
    
