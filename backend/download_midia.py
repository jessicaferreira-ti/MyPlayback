import os
import sys
import subprocess

# Certifique-se de que o pytube está instalado corretamente
try:
    from pytubefix import YouTube # This is solution
    # import pytube
    # from pytube import YouTube
except ModuleNotFoundError:
    print("pytube não encontrado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytube"])
    import pytube
    from pytube import YouTube

# Obtém o diretório de Downloads do usuário de forma multiplataforma
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

def baixar_video(youtube_url):
    try:
        yt = YouTube(youtube_url)
        video = yt.streams.filter(file_extension="mp4", progressive=True).get_highest_resolution()
        print(f"Baixando: {yt.title}...")
        video.download(DOWNLOADS_FOLDER)
        print(f"Download concluído! Arquivo salvo em: {DOWNLOADS_FOLDER}")
    except pytube.exceptions.VideoUnavailable:
        print("Erro: O vídeo não está disponível.")
    except pytube.exceptions.PytubeError as e:
        print(f"Erro do pytube: {e}")
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {e}")

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=TYUL383IcKA&ab_channel=MariaAlice" #input("Digite a URL do vídeo do YouTube: ")
    baixar_video(url)
