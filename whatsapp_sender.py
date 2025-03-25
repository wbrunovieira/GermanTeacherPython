import os
import requests
import logging

Bruno_WHATSAPP_API_KEY = os.getenv("Bruno_WHATSAPP_API_KEY")
WB_WHATSAPP_INSTANCE_ID = os.getenv("WB_WHATSAPP_INSTANCE_ID")

if not Bruno_WHATSAPP_API_KEY or not WB_WHATSAPP_INSTANCE_ID:
    raise ValueError("Defina Bruno_WHATSAPP_API_KEY e WB_WHATSAPP_INSTANCE_ID no .env")

API_BASE_URL   = "https://whatsapp-api.wbdigitalsolutions.com"
MEDIA_BASE_URL = "https://wbdevaudio.loca.lt"  # LocalTunnel URL

ENDPOINT = f"{API_BASE_URL}/message/sendMedia/{WB_WHATSAPP_INSTANCE_ID}"

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

def enviar_audio_whatsapp(numero_whatsapp, caminho_audio, caption="Aqui está seu áudio!"):
    file_name = os.path.basename(caminho_audio)
    media_url = f"{MEDIA_BASE_URL}/audios/{file_name}"

    payload = {
        "number": numero_whatsapp,
        "mediatype": "audio",
        "mimetype": "audio/mpeg",
        "caption": caption,
        "media": media_url,
        "fileName": file_name
    }
    headers = {
    "apikey": Bruno_WHATSAPP_API_KEY,
    "Content-Type": "application/json"
}
    logging.debug("POST %s\nHeaders: %s\nPayload: %s", ENDPOINT, headers, payload)

    resp = requests.post(ENDPOINT, headers=headers, json=payload)
    logging.debug("Response %s: %s", resp.status_code, resp.text)
    if resp.status_code == 200:
        print("Áudio enviado com sucesso!")
    else:
        print(f"Erro {resp.status_code}: {resp.text}")
    return resp.json()