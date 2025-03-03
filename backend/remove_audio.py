import os
from moviepy.editor import VideoFileClip

def remove_audio(video_path, output_dir="outputs/midias_sem_audio"):
    """Remove o áudio do vídeo e salva como MP3 sem chamar FFmpeg diretamente."""
    os.makedirs(output_dir, exist_ok=True)

    video_output_path = os.path.join(output_dir, "video_sem_audio.mp4")
    audio_output_path = os.path.join(output_dir, "som_extraido.mp3")

    try:
        # Carrega o vídeo
        video = VideoFileClip(video_path)

        # Se houver áudio, extrai como MP3
        if video.audio is not None:
            video.audio.write_audiofile(audio_output_path, codec="mp3")
        else:
            print("⚠️ O vídeo não tem faixa de áudio. Nenhum MP3 será gerado.")
            audio_output_path = None  # Evita erro

        # Remove o áudio do vídeo
        video = video.without_audio()
        video.write_videofile(video_output_path, codec="libx264")

        return video_output_path, audio_output_path

    except Exception as e:
        raise Exception(f"Erro ao processar o vídeo: {e}")

if __name__ == "__main__":
    video_path = ".outputs/videos_baixados/Believer - First 1 minute.mp4" # Substitua pela URL correta
    try:
        video_sem_audio, audio_mp3 = remove_audio(video_path)
        print(f"✅ Vídeo sem áudio salvo em: {video_sem_audio}")
        if audio_mp3:
            print(f"✅ Áudio salvo em MP3 em: {audio_mp3}")
    except Exception as e:
        print(f"❌ Erro ao remover áudio: {e}")
