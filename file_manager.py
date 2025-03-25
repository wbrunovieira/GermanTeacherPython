
# file_manager.py
import os
import re
import time
from urllib.parse import urlparse

import requests

import base64
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

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


def descriptografar_audio(arquivo_encriptado, mediaKey, output_filename=None):
    """
    Descriptografa o arquivo de áudio baixado (com extensão .enc) utilizando a mediaKey.
    
    Parâmetros:
      - arquivo_encriptado: caminho do arquivo encriptado (baixado do WhatsApp)
      - mediaKey: chave de mídia (em formato base64) extraída do payload
      - output_filename: (opcional) nome para salvar o arquivo descriptografado. 
                         Se não fornecido, o nome será derivado do arquivo_encriptado.
    
    Retorna:
      - output_filename: caminho do arquivo descriptografado.
    """
    # Ler o conteúdo do arquivo encriptado
    with open(arquivo_encriptado, "rb") as f:
        data = f.read()

    # Remover os últimos 10 bytes (MAC) que não fazem parte da encriptação
    data = data[:-10]

    # Decodificar a mediaKey que vem em base64
    mediaKey_bytes = base64.b64decode(mediaKey)

    # Derivar as chaves utilizando HKDF.
    # Para áudios, usamos o parâmetro info "WhatsApp Audio Keys" e derivamos 80 bytes:
    # - IV: primeiros 16 bytes
    # - Chave de cifra (cipherKey): próximos 32 bytes
    # - (Os 32 bytes restantes seriam para MAC, mas não serão usados aqui)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=80,
        salt=None,
        info=b"WhatsApp Audio Keys",
    )
    derived = hkdf.derive(mediaKey_bytes)
    iv = derived[0:16]
    cipherKey = derived[16:48]

    # Cria o objeto de cifra com AES em modo CBC e decripta os dados
    cipher = AES.new(cipherKey, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(data)

    # Remove o padding PKCS7
    padding_len = decrypted[-1]
    decrypted = decrypted[:-padding_len]

    # Define o nome do arquivo descriptografado, se não for passado
    if output_filename is None:
        # Supondo que o áudio seja .ogg; ajuste conforme necessário
        output_filename = arquivo_encriptado.replace(".enc", "_dec.ogg")
    
    # Salva o áudio descriptografado
    with open(output_filename, "wb") as f:
        f.write(decrypted)

    print(f"Áudio descriptografado salvo em: {output_filename}")
    return output_filename