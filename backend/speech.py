import speech_recognition as sr
from voice import say_tts as say
from youtubeplay import play_video
import os

song_playing = False


def do_action(sentence: str) -> None:
    global song_playing

    mikoIndex = sentence.lower().find('miko')
    sentence = sentence[mikoIndex + 4:].strip()

    if song_playing and sentence.startswith('stop'):
        say("Okay, I will stop the song")
        os.system("pkill mpv")
        song_playing = False
        return

    song = sentence[4:].strip() if sentence.lower(
    ).startswith('play') else sentence
    say(f"Okay, I will play {song}")
    title = play_video(song)

    if title:
        say(f"Now playing {title}")
        song_playing = True
    else:
        say("Sorry, I couldn't find the song you asked for")
        song_playing = False


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
            sentence = result['transcript']
            if sentence.lower().startswith('miko'):
                return sentence
    except Exception as e:
        print("Error: ", e)

    return ''


if __name__ == "__main__":
    while True:
        sentence = recognize_voice()
        if sentence:
            do_action(sentence)
