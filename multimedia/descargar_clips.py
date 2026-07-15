import yt_dlp
import os
import shutil

urls = [
    "https://www.youtube.com/watch?v=kG82iT624l0",
    "https://www.youtube.com/watch?v=Fj-y57U2t-g",
    "https://www.youtube.com/watch?v=2TzT3k1R3yE"
]

download_path = r"D:\Downloads"
target_path = r"D:\Videos\DaVinci Resolve\B-Rolls_Stock_Anime"

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(urls)

# Mover a target
for filename in os.listdir(download_path):
    if filename.endswith(".mp4"):
        shutil.move(os.path.join(download_path, filename), os.path.join(target_path, filename))
