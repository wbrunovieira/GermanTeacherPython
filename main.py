#main.py
from flask import Flask, jsonify
from flask import send_from_directory
from config import carregar_configuracoes
from data_handler import ler_tempos_json, salvar_tempos_json, buscar_e_atualizar_primeiro_tema
from api_client import gerar_texto_aula
from file_manager import salvar_texto_em_diretorio
from audio_generator import gerar_audio_com_elevenlabs
from whatsapp_sender import enviar_audio_whatsapp


import os

import openai

app = Flask(__name__)
numero_whatsapp = "5511982864581"

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)