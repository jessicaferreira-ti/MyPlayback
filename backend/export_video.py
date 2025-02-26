from moviepy.editor import VideoFileClip

def export_video(video_path, output_path="video_final.mp4"):
    video = VideoFileClip(video_path)
    video.write_videofile(output_path)
    return output_path