from pytube import Search, YouTube
from multiprocessing import Process
import os


def play_video(video: str):
    s = Search(video)
    result: YouTube = s.results[0]
    filename: str = result.title + '.mp4'
    os.chdir(os.path.expanduser("~/Downloads"))

    if os.path.exists(filename):
        print("File already exists")
    else:
        result.streams.filter(only_audio=True, file_extension='mp4').first().download()

    Process(target=os.system, args=(f"mpv '{filename.replace(',', '')}' --volume=50",)).start()
    return result.title


if __name__ == "__main__":
    play_video("Ob-La-Di, Ob-La-Da")
