from pytube import Search, YouTube
from multiprocessing import Process
from func.moduler import module_path
import re
import os


def play_video(video: str):
    s = Search(video)
    result: YouTube = s.results[0]

    if 'musicVideoType' not in result.vid_info['videoDetails']:
        return ''

    path = module_path('audio', __name__)

    if not os.path.exists(path):
        os.mkdir(path)

    audio = result.streams.filter(only_audio=True, file_extension='mp4').first()
    filename = re.sub(r"[^\w ()-]", '', result.title) + '.mp4'
    audio.download(output_path=path, filename=filename)
    Process(target=os.system, args=(f"mpv '{path}/{filename}'",)).start()
    return result.title


if __name__ == "__main__":
    # play_video("Ob-la-di Ob-la-da")
    # play_video("Octupus's Garden")
    # play_video("Come sweet death")
    play_video("Kizuna AI")
