from moviepy.editor import VideoFileClip

def remove_audio(video_path, output_path="video_sem_audio.mp4"):
    video = VideoFileClip(video_path)
    video = video.without_audio()
    video.write_videofile(output_path)
    return output_path