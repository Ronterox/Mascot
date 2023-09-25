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

    if re.search(r'turn off|shutdown', sentence):
        os.system('shutdown 0')
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
        results = r.recognize_google(audio, show_all=True, language='en-US')
        print("Results: ", len(results['alternative']))
        best_sentence = ''
        max_points = -1
        for result in results['alternative']:
            sentence: str = result['transcript']
            found = re.search(r'[mn][ie]{1,2}[kc]{1,2}[aeiou]', sentence.lower())
            if found:
                miko = "".join(dict.fromkeys(found[0]))
                points = 0
                if miko[0] == 'm':
                    points += 5
                if miko[1] == 'i':
                    points += 5
                if miko[2] == 'k':
                    points += 5
                if miko[3] == 'o':
                    points += 5
                elif miko[3] == 'u':
                    points += 3
                if points > max_points:
                    best_sentence = sentence
                    max_points = points
                print(f"[Miko ({points})]", sentence)
            else:
                print("[Not Miko]", sentence)
        return best_sentence
    except Exception as e:
        print("Error: ", e)

    return ''


if __name__ == "__main__":
    while True:
        sentence = recognize_voice()
        if sentence:
            do_action(sentence)
