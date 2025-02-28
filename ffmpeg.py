import subprocess

try:
    subprocess.run(["ffmpeg", "-version"], check=True)
    print("FFmpeg está instalado corretamente!")
except FileNotFoundError:
    print("FFmpeg ainda não está acessível pelo Python.")
