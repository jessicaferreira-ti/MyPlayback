import os
import subprocess
import uuid
from transformers import pipeline

def split_audio(video_path, output_dir="outputs/audio_chunks", chunk_length=30):
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

def generate_subtitles(video_path, output_dir="outputs/subtitles"):
    """Gera legendas no formato SRT."""
    try:
        os.makedirs(output_dir, exist_ok=True)

        # Divide o áudio em partes menores
        audio_chunks = split_audio(video_path)

        # Carrega o modelo Whisper
        model = pipeline("automatic-speech-recognition", model="openai/whisper-small")

        subtitles = []
        start_time = 0.0
        chunk_duration = 30.0  # Duração fixa de cada trecho em segundos

        for idx, chunk in enumerate(audio_chunks):
            result = model(chunk, return_timestamps=True)

            if "chunks" in result:
                for segment in result["chunks"]:
                    # ✅ Garante que os timestamps não sejam None
                    start = start_time + (segment["timestamp"][0] if segment["timestamp"][0] is not None else 0.0)
                    end = start_time + (segment["timestamp"][1] if segment["timestamp"][1] is not None else 0.0)
                    text = segment["text"].strip()

                    subtitles.append(f"{idx+1}\n{format_timestamp(start)} --> {format_timestamp(end)}\n{text}\n")

            # Atualiza tempo inicial para o próximo trecho
            start_time += chunk_duration

        # Salva o arquivo SRT
        output_filename = f"subtitles_{uuid.uuid4().hex}.srt"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(subtitles))

        return output_path

    except Exception as e:
        raise Exception(f"Erro ao gerar legendas: {e}")


if __name__ == "__main__":
    video_path = ".outputs/videos_baixados/Believer - First 1 minute.mp4" # Substitua pela URL correta
    try:
        subtitles_path = generate_subtitles(video_path)
        print(f"Legendas geradas e salvas em: {subtitles_path}")
    except Exception as e:
        print(e)
