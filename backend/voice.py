from multiprocessing import Process
from TTS.api import TTS
from func.moduler import module_path
import os

model_name = TTS.list_models()[0]
tts = TTS(model_name, gpu=True)
lang = tts.languages[0]
speaker = tts.speakers[2]

AUDIO_PATH = module_path("audio", __name__)
SAMPLE_PATH = f"{AUDIO_PATH}/miku.wav"
OUTPUT_PATH = f"{AUDIO_PATH}/output.wav"

def say_tts(text):
    try:
        tts.tts_to_file(text, language=lang, speaker_wav=SAMPLE_PATH, file_path=OUTPUT_PATH)
        Process(target=os.system, args=(f"amixer set Master 50% && aplay {OUTPUT_PATH}",)).start()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    say_tts("Hello, world!")