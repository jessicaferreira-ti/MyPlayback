from pytubefix import YouTube
import re

# Função para corrigir a URL
def corrigir_url(url):
    padrao = re.compile(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*')
    match = padrao.search(url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        raise ValueError("URL do YouTube inválida.")

# Função para baixar vídeo
def download_video(url, output_path="videos_baixados"):
    try:
        url_corrigida = corrigir_url(url)
        yt = YouTube(url_corrigida)
        stream = yt.streams.filter(file_extension='mp4').first()
        stream.download(output_path)
        return output_path
    except Exception as e:
        raise Exception(f"Erro ao baixar o vídeo: {e}")