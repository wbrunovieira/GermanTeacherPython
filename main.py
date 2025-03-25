#main.py

from urllib.parse import urlparse
from flask import Flask, jsonify, request
from flask import send_from_directory

from config import carregar_configuracoes
from data_handler import ler_tempos_json,  salvar_tempos_json, buscar_e_atualizar_primeiro_tema
from api_client import gerar_texto_aula
from file_manager import salvar_audio_na_pasta, salvar_texto_em_diretorio
from audio_generator import gerar_audio_com_elevenlabs
from whatsapp_sender import enviar_audio_whatsapp, enviar_texto_whatsapp


import os

import openai

app = Flask(__name__)
numero_whatsapp = "5511982864581"
numero_whatsappGaga = "34674804376"



@app.route('/audios/<path:filename>')
def serve_audio(filename):
    return send_from_directory('teacher_audios', filename)

@app.route('/gerar_aula', methods=['GET'])
def gerar_aula():
    try:
        api_key = carregar_configuracoes()
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    temas = ler_tempos_json()
    tema = buscar_e_atualizar_primeiro_tema(temas)
    
    if not tema:
        return jsonify({"message": "Todos os temas já foram executados."})
    
    salvar_tempos_json(temas)
    
    texto_aula = gerar_texto_aula(client, tema)
    

    if texto_aula:
        caminho_salvo = salvar_texto_em_diretorio(texto_aula, tema)
        
        try:
            resultado_texto = enviar_texto_whatsapp(numero_whatsapp, texto_aula)
            print("Resultado do envio de texto:", resultado_texto)
            nome_base = os.path.splitext(os.path.basename(caminho_salvo))[0]
            caminho_audio = gerar_audio_com_elevenlabs(texto_aula, nome_base)
            if caminho_audio:
              resultado_envio = enviar_audio_whatsapp(numero_whatsapp, caminho_audio)
              print("Resultado do envio:", resultado_envio)

        except Exception as e:
            print(f"Erro ao gerar áudio: {e}")
            caminho_audio = None

        return jsonify({
            "tema": tema,
            "texto_aula": texto_aula,
            "caminho_texto": caminho_salvo,
            "caminho_audio": caminho_audio
        })



@app.route('/webhook/messages_upsert', methods=['POST'])
def whatsapp_webhook():
    print("Payload recebido:", request.json)
    payload = request.json
    messages = payload.get('messages')
    if not messages and 'data' in payload:
        messages = [payload['data']]
    

    allowed_numbers = [numero_whatsapp, numero_whatsappGaga]
    
    for msg in messages:
        if msg.get('messageType') != 'audioMessage':
            continue  
        

        sender_id = msg['key'].get('participant', msg['key'].get('remoteJid'))
        phone_number = sender_id.split('@')[0]
        
        if phone_number not in allowed_numbers:
            print(f"Ignorando áudio de usuário não permitido: {phone_number}")
            continue  
        
        audio_url = msg['message']['audioMessage']['url']
        print(f"Áudio recebido de {sender_id}: {audio_url}")
        try:
            salvar_audio_na_pasta(audio_url, sender_id)
        except Exception as e:
            print(f"Erro ao salvar áudio: {e}")
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)