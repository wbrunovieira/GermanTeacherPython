from flask import Flask, jsonify
from config import carregar_configuracoes
from data_handler import ler_tempos_json, salvar_tempos_json, buscar_e_atualizar_primeiro_tema
from api_client import gerar_texto_aula
from file_manager import salvar_texto_em_diretorio
import openai

app = Flask(__name__)

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
        return jsonify({
            "tema": tema,
            "texto_aula": texto_aula,
            "caminho_salvo": caminho_salvo
        })
    return jsonify({"error": "Falha ao gerar texto da aula"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)