import os
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip

def remove_vocal_keep_instrumental(video_path, output_dir = os.path.normpath("outputs/midias_processadas")):
    """Remove apenas a voz do áudio do vídeo e mantém a parte instrumental usando Demucs."""
    os.makedirs(output_dir, exist_ok=True)

    video_output_path = os.path.join(output_dir, "video_sem_voz.mp4")
    print(video_output_path)
    extracted_audio_path = os.path.join(output_dir, "audio_original.mp3")
    print(extracted_audio_path)
    instrumental_audio_path = os.path.join(output_dir, "instrumental.wav")
    print(instrumental_audio_path)

    try:
        # Carrega o vídeo
        video = VideoFileClip(video_path)

        if video.audio is None:
            print("⚠️ O vídeo não tem áudio. Nada será processado.")
            return None, None

        # Salva o áudio original
        video.audio.write_audiofile(extracted_audio_path, codec="mp3")

        # Usa Demucs para separar voz e instrumental
        print("🎵 Separando áudio com Demucs...")
        subprocess.run(f'demucs -n htdemucs "{extracted_audio_path}"', shell=True, check=True)


        # Localiza o arquivo instrumental gerado pelo Demucs
        demucs_output_dir = os.path.normpath(os.path.join("separated", "htdemucs", os.path.basename(extracted_audio_path).replace(".mp3", "")))
        instrumental_path = os.path.join(demucs_output_dir, "no_vocals.wav")

        if not os.path.exists(instrumental_path):
            raise Exception("Erro na separação de áudio. Verifique a saída do Demucs.")

        # Renomeia e move o instrumental para a pasta de saída
        os.rename(instrumental_path, instrumental_audio_path)

        # Adiciona o áudio instrumental de volta ao vídeo
        instrumental_audio = AudioFileClip(instrumental_audio_path)
        video = video.set_audio(instrumental_audio)
        video.write_videofile(video_output_path, codec="libx264", audio_codec="aac")

        return video_output_path, instrumental_audio_path

    except Exception as e:
        raise Exception(f"Erro ao processar o vídeo: {e}")

if __name__ == "__main__":
    video_path = "outputs/videos_baixados/Believer - First 1 minute.mp4"  # Substitua pelo caminho correto
    try:
        video_sem_voz, instrumental_mp3 = remove_vocal_keep_instrumental(video_path)
        print(f"✅ Vídeo sem voz salvo em: {video_sem_voz}")
        print(f"✅ Áudio instrumental salvo em: {instrumental_mp3}")
    except Exception as e:
        print(f"❌ Erro: {e}")
