from transformers import pipeline

def generate_subtitles(video_path):
    model = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    result = model(video_path)
    return result["text"]