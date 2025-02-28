import torch
import streamlit as st
import sys
import os

torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)] 

# or simply:
torch.classes.__path__ = []

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.download_video import download_video
from backend.generate_subtitles import generate_subtitles
from backend.remove_audio import remove_audio
from backend.add_audio import add_audio
from backend.add_subtitles import add_subtitles
from backend.export_video import export_video

# Título da aplicação
st.title("Editor de Vídeo com IA")

# Input para URL do YouTube
url = st.text_input("Cole a URL do YouTube aqui")
url = "https://www.youtube.com/watch?v=gDXhFrYuZ7I"

if  url:
    # Exibe o vídeo do YouTube
    st.video(url)

    # Botão para baixar o vídeo
    if st.button("Baixar Vídeo"):
        video_path = download_video(url)
        st.success(f"Vídeo baixado e salvo em: {video_path}")
        st.session_state['video_path'] = video_path  # Salva o caminho do vídeo na sessão

    # Botão para gerar legendas
    if st.button("Gerar Legendas Automáticas") and 'video_path' in st.session_state:
        # subtitles = generate_subtitles(st.session_state['video_path'])
        # st.text_area("Legendas Geradas", subtitles)
        # st.session_state['subtitles'] = subtitles  # Salva as legendas na sessão
        
        try:
            subtitles_path = generate_subtitles(st.session_state['video_path'])
            st.success(f"Legendas geradas e salvas em: {subtitles_path}")
            with open(subtitles_path, "r", encoding="utf-8") as f:
                subtitles = f.read()
            st.text_area("Legendas Geradas", subtitles)
            st.session_state['subtitles'] = subtitles  # Salva as legendas na sessão
        except Exception as e:
            st.error(f"Erro ao gerar legendas: {e}")

    # Botão para remover áudio
    if st.button("Remover Áudio") and 'video_path' in st.session_state:
        video_sem_audio = remove_audio(st.session_state['video_path'])
        st.success(f"Áudio removido. Vídeo salvo em: {video_sem_audio}")
        st.session_state['video_sem_audio'] = video_sem_audio

    # Botão para adicionar novo áudio
    if st.button("Adicionar Novo Áudio") and 'video_sem_audio' in st.session_state:
        audio_path = st.file_uploader("Faça upload do arquivo de áudio (instrumental)", type=["mp3", "wav"])
        print('audio_path', audio_path)
        if audio_path:
            video_com_audio = add_audio(st.session_state['video_sem_audio'], audio_path)
            st.success(f"Novo áudio adicionado. Vídeo salvo em: {video_com_audio}")
            st.session_state['video_com_audio'] = video_com_audio

    # Botão para adicionar legendas ao vídeo
    if st.button("Adicionar Legendas ao Vídeo") and 'video_com_audio' in st.session_state and 'subtitles' in st.session_state:
        video_com_legendas = add_subtitles(st.session_state['video_com_audio'], st.session_state['subtitles'])
        st.success(f"Legendas adicionadas. Vídeo salvo em: {video_com_legendas}")
        st.session_state['video_com_legendas'] = video_com_legendas

    # Botão para exportar vídeo final
    if st.button("Exportar Vídeo Final") and 'video_com_legendas' in st.session_state:
        video_final = export_video(st.session_state['video_com_legendas'])
        st.success(f"Vídeo final exportado: {video_final}")
        st.video(video_final)  # Exibe o vídeo final