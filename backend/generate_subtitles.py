import os
import uuid
from transformers import pipeline

# Função para gerar legendas a partir de um arquivo de vídeo
def generate_subtitles(video_path, output_dir="subtitles"):
    try:
        # Cria o diretório de saída, se não existir
        os.makedirs(output_dir, exist_ok=True)

        # Gera um nome de arquivo único para as legendas
        output_filename = f"subtitles_{uuid.uuid4().hex}.txt"
        output_path = os.path.join(output_dir, output_filename)

        # Carrega o modelo de geração de legendas (Whisper, por exemplo)
        model = pipeline("automatic-speech-recognition", model="openai/whisper-small")

        # Gera as legendas a partir do áudio do vídeo
        result = model(video_path)
        subtitles = result["text"]

        # Salva as legendas em um arquivo de texto
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(subtitles)

        return output_path
    except Exception as e:
        raise Exception(f"Erro ao gerar legendas: {e}")

# Exemplo de uso (para testes)
if __name__ == "__main__":
    video_path = "videos_baixados"  # Substitua pelo caminho do vídeo
    try:
        subtitles_path = generate_subtitles(video_path)
        print(f"Legendas geradas e salvas em: {subtitles_path}")
    except Exception as e:
        print(e)