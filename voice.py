from multiprocessing import Process
from TTS.api import TTS
import os

model_name = TTS.list_models()[0]
tts = TTS(model_name, gpu=True)
lang = tts.languages[0]
speaker = tts.speakers[2]

def say_tts(text):
    try:
        tts.tts_to_file(text, language=lang, speaker_wav="miku.wav", file_path="output.wav")
        Process(target=os.system, args=("aplay output.wav",)).start()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    say_tts("Hello, world!")