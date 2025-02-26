from pytube import YouTube

def download_video(url, output_path="video.mp4"):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4').first()
    stream.download(output_path)
    return output_path