from moviepy.editor import VideoFileClip

def export_video(video_path, output_path="outputs/video_final"):
    video = VideoFileClip(video_path)
    video.write_videofile(output_path)
    return output_path