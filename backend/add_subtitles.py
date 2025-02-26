from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip

def add_subtitles(video_path, subtitles, output_path="video_com_legendas.mp4"):
    video = VideoFileClip(video_path)
    txt_clip = TextClip(subtitles, fontsize=24, color='white')
    txt_clip = txt_clip.set_position('bottom').set_duration(video.duration)
    final_video = CompositeVideoClip([video, txt_clip])
    final_video.write_videofile(output_path)
    return output_path