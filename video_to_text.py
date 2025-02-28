import os
import subprocess
import uuid
from transformers import pipeline

def split_audio(video_path, output_dir="audio_chunks", chunk_length=30):
    """Divide o áudio do vídeo em trechos menores de X segundos usando FFmpeg."""
    os.makedirs(output_dir, exist_ok=True)
    output_format = os.path.join(output_dir, "chunk_%03d.wav")

    command = [
        "ffmpeg", "-i", video_path, "-f", "segment", "-segment_time", str(chunk_length),
        "-ac", "1", "-ar", "16000", "-c", "pcm_s16le", output_format
    ]

    subprocess.run(command, check=True)

    return sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".wav")])

def format_timestamp(seconds):
    """Converte tempo em segundos para o formato SRT (HH:MM:SS,ms)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def generate_subtitles(video_path, output_dir="subtitles"):
    """Gera legendas no formato SRT."""
    try:
        os.makedirs(output_dir, exist_ok=True)

        # Divide o áudio em partes menores
        audio_chunks = split_audio(video_path)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_path = "./videos_baixados/Ouvidos pra Te ouvir - Thamires Garcia feat Simone Paulino.mp4" # Substitua pela URL correta
    try:
        subtitles_path = generate_subtitles(video_path)
        print(f"Legendas geradas e salvas em: {subtitles_path}")
    except Exception as e:
        print(e)
       
