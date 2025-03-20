import json
import os
from datetime import datetime
import openai
from config import carregar_configuracoes
from flask import Flask, jsonify

app = Flask(__name__)

def ler_tempos_json(caminho='temas.json'):
    """Lê o arquivo JSON contendo os temas."""
    with open(caminho, 'r', encoding='utf-8') as file:
        temas = json.load(file)
    return temas

def salvar_tempos_json(temas, caminho='temas.json'):
    """Salva a lista de temas atualizada no arquivo JSON."""
    with open(caminho, 'w', encoding='utf-8') as file:
        json.dump(temas, file, ensure_ascii=False, indent=4)

def buscar_e_atualizar_primeiro_tema(temas):
    """Busca e atualiza o primeiro tema não executado."""
    for item in temas:
        if not item.get("executado", False):
            item["executado"] = True
            item["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return item["tema"]
    return None

def gerar_texto_aula(client, tema):
    """Gera o texto de aula utilizando a API da Deepseek."""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Você é uma professora de alemão chamada Greta."},
                {"role": "user", "content": (
                    f"Crie uma lição simples de alemão para iniciantes, focando no tema '{tema}'. "
                    "Inclua exemplos práticos e palavras básicas. "
                    "Escreva o texto de forma amigável, com no mínimo 500 caracteres e no máximo 1000 caracteres, "
                    "para facilitar a geração de áudio."
                )}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro na comunicação com a Deepseek: {e}")
        return None

def salvar_texto_em_diretorio(texto, tema, diretorio="teacher_texts"):
    """Salva o texto gerado em um arquivo."""
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    nome_arquivo = f"{tema.lower().replace(' ', '_')}.txt"
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(texto)
    
    return caminho_arquivo

@app.route('/gerar_aula', methods=['GET'])

@app.route('/gerar_aula', methods=['GET'])
def gerar_aula():
    try:
        # Configuração corrigida
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
    
    # CORREÇÃO AQUI: Passar client e tema como argumentos
    texto_aula = gerar_texto_aula(client, tema)  # <--- Parâmetros adicionados
    
    if texto_aula:
        caminho_salvo = salvar_texto_em_diretorio(texto_aula, tema)
        return jsonify({
            "tema": tema,
            "texto_aula": texto_aula,
            "caminho_salvo": caminho_salvo
        })
    return jsonify({"error": "Falha ao gerar texto da aula"}), 500

def gerar_texto_aula(client, tema):
    """Gera texto usando Deepseek R1"""
    try:
        response = client.chat.completions.create(
             model="deepseek-chat", 
            messages=[
                {"role": "system", "content": "Você é uma professora de alemão chamada Greta."},
                {"role": "user", "content": (
                    f"Crie uma lição simples de alemão para iniciantes no tema '{tema}'. "
                    "Inclua exemplos práticos e palavras básicas. Formato amigável, "
                    "500-1000 caracteres para facilitar conversão em áudio."
                )}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro Deepseek: {e}")
        return None
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)