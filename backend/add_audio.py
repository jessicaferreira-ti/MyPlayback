import os
from moviepy.editor import VideoFileClip, AudioFileClip

def add_audio(video_path, audio_path, output_dir="outputs/add_audio"):
    """Adiciona um novo áudio a um vídeo."""
    os.makedirs(output_dir, exist_ok=True)  # Cria a pasta de saída se não existir

    # Caminho do arquivo de saída
    output_path = os.path.join(output_dir, "video_com_audio.mp4")

    # Carregar o vídeo e áudio
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Ajusta a duração do áudio para combinar com o vídeo
    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)  # Corta o áudio para a duração do vídeo
    elif audio.duration < video.duration:
        print("⚠️ Aviso: O áudio é menor que o vídeo. O vídeo pode ficar sem som no final.")

    # Define o áudio no vídeo
    video = video.set_audio(audio)

    # Salva o vídeo com o novo áudio
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path

if __name__ == "__main__":
    video_path = "caminho/do/video.mp4"  # Substitua pelo caminho correto
    audio_path = "caminho/do/audio.mp3"  # Substitua pelo caminho correto
    try:
        output_video = add_audio(video_path, audio_path)
        print(f"✅ Vídeo com áudio salvo em: {output_video}")
    except Exception as e:
        print(f"❌ Erro ao adicionar áudio: {e}")
