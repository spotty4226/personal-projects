from yt_dlp import YoutubeDL

def download_video(link):
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

link = input("Enter the YouTube link you wish to download: ")
download_video(link)
