import speech_recognition as sr
from voice import say_tts
from youtubeplay import play_video
import re
import os


song_playing = False


def say(txt: str) -> None:
    print(txt)
    say_tts(txt)


def close_mpv() -> None:
    global song_playing
    os.system("pkill mpv")
    song_playing = False


def do_action(sentence: str) -> None:
    global song_playing

    mikoIndex = sentence.lower().find('miko')
    sentence = sentence[mikoIndex + 4:].strip()

    if not sentence or song_playing and sentence == 'stop':
        say("Okay, I will stop the song")
        close_mpv()
        return

    song = sentence[4:].strip() if sentence.lower(
    ).startswith('play') else sentence
    say(f"Okay, I will play {song}")

    if song_playing:
        close_mpv()

    title = play_video(song)

    if title:
        say(f"Now playing {title}")
        song_playing = True
    else:
        say("Sorry, I couldn't find the song you asked for")
        close_mpv()


def recognize_voice() -> str:
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, phrase_time_limit=5)
        print("Done!")

    try:
        results = r.recognize_google(audio, show_all=True)
        print("Results: ", len(results['alternative']))
        for result in results['alternative']:
            sentence: str = result['transcript']
            if re.search(r'mik[aeiou]', sentence.lower()):
                print("[Miko]", sentence)
                return sentence
            else:
                print("[Not Miko]", sentence)
    except Exception as e:
        print("Error: ", e)

    return ''


if __name__ == "__main__":
    while True:
        sentence = recognize_voice()
        if sentence:
            do_action(sentence)
