
# file_manager.py
import os
import re
import time
from urllib.parse import urlparse

import requests

def salvar_texto_em_diretorio(texto, tema, diretorio="teacher_texts"):
    """Salva o texto gerado em um arquivo."""
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    nome_arquivo = re.sub(r'[^\w\s-]', '', tema.lower())  # remove parênteses, barras, etc.
    nome_arquivo = nome_arquivo.replace(' ', '_') + ".txt"

    caminho_arquivo = os.path.join(diretorio, nome_arquivo)

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(texto)

    return caminho_arquivo


def salvar_audio_na_pasta(audio_url, sender):
    os.makedirs("student_audios", exist_ok=True)
    filename = os.path.basename(urlparse(audio_url).path)
    # Corrige o caminho trocando audios_teacher por audios
    download_url = audio_url.replace("/audios_teacher/", "/audios/")

    filepath = os.path.join(
        "student_audios",
        f"{sender.replace('@','_')}_{int(time.time())}{os.path.splitext(filename)[1]}"
    )

    print("download_url", download_url)
    resp = requests.get(download_url)
    print("Status code:", resp.status_code)
    resp.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(resp.content)

    print(f"Áudio salvo em: {filepath}")
    return filepath