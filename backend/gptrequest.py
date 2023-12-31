import requests

# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/generate'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'

def predict(prompt):
    request = {
        'prompt': prompt,
        'max_new_tokens': 120,
        'do_sample': True,
        'temperature': 0.5,
        'top_p': 0.1,
        'typical_p': 1,
        'repetition_penalty': 1.15,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    try:
        response = requests.post(URI, json=request)
    except requests.exceptions.ConnectionError:
        return None

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        print(f"Prompt: {prompt}\nResult: {result}")
        return result
    return None

if __name__ == '__main__':
    prompt = "In order to make homemade bread, follow these steps:\n1)"
    predict(prompt)
