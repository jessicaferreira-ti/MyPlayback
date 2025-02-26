from moviepy.editor import VideoFileClip, AudioFileClip

def add_audio(video_path, audio_path, output_path="video_com_audio.mp4"):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path)
    return output_path