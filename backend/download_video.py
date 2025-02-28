import os
from pytubefix import YouTube
import re

def corrigir_url(url):
    padrao = re.compile(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*')
    match = padrao.search(url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        raise ValueError("URL do YouTube inválida.")

def download_video(url, output_path="videos_baixados"):
    try:
        url_corrigida = corrigir_url(url)
        yt = YouTube(url_corrigida)
        stream = yt.streams.filter(file_extension='mp4').first()
        
        # Garante que o diretório existe
        os.makedirs(output_path, exist_ok=True)

        # Baixa o vídeo e retorna o caminho completo
        video_path = stream.download(output_path)
        return video_path  # Retorna o caminho completo do vídeo
    except Exception as e:
        raise Exception(f"Erro ao baixar o vídeo: {e}")
