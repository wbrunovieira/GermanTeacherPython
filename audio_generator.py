# audio_generator.py

import os
import requests
from dotenv import load_dotenv


load_dotenv()

def gerar_audio_com_elevenlabs(texto: str, nome_arquivo: str, diretorio: str = "teacher_audios") -> str:
    """
    Gera áudio a partir de um texto usando a API da ElevenLabs e salva como .mp3.

    Args:
        texto (str): Texto que será convertido em áudio.
        nome_arquivo (str): Nome do arquivo mp3 (sem extensão).
        diretorio (str): Pasta onde o áudio será salvo.

    Returns:
        str: Caminho completo do arquivo de áudio salvo.
    """
    print(">>> Iniciando geração de áudio com ElevenLabs...")
    print(">>> [audio_generator.py] módulo carregado!")

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("Chave da ElevenLabs não encontrada no .env.")

    print(">>> [✓] API Key carregada.")
    print(f">>> [📝] Tamanho do texto: {len(texto)} caracteres")

 
    voice_id = "EXAVITQu4vr4xnSDxMaL"


    os.makedirs(diretorio, exist_ok=True)


    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

 
    body = {
        "text": texto,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }

    print(">>> Enviando requisição para ElevenLabs...")
    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro na requisição para ElevenLabs: {e}")

    if response.status_code == 200:
        caminho_audio = os.path.join(diretorio, f"{nome_arquivo}.mp3")
        with open(caminho_audio, "wb") as f:
            f.write(response.content)
        print(f">>> Áudio salvo em: {caminho_audio}")
        return caminho_audio
    else:
        print(">>> Erro na resposta da ElevenLabs:", response.status_code, response.text)
        raise Exception(f"Erro na ElevenLabs: {response.status_code} - {response.text}")