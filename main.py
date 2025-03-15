# main.py
import json
import os
from datetime import datetime
import openai
from config import carregar_configuracoes

def ler_tempos_json(caminho='temas.json'):
    """
    Lê o arquivo JSON contendo os temas.
    """
    with open(caminho, 'r', encoding='utf-8') as file:
        temas = json.load(file)
    return temas

def salvar_tempos_json(temas, caminho='temas.json'):
    """
    Salva a lista de temas atualizada no arquivo JSON.
    """
    with open(caminho, 'w', encoding='utf-8') as file:
        json.dump(temas, file, ensure_ascii=False, indent=4)

def buscar_e_atualizar_primeiro_tema(temas):
    """
    Busca o primeiro tema que ainda não foi executado, atualiza seu status e data.
    Retorna o tema encontrado (ou None, se todos já tiverem sido executados).
    """
    for item in temas:
        if not item.get("executado", False):
            item["executado"] = True
            item["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return item["tema"]
    return None

def gerar_texto_aula(tema):
    """
    Função para gerar texto de aula utilizando o modelo da OpenAI.
    Inclui restrições de tamanho e tom amigável para facilitar a geração de áudio.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
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
        message_text = response.choices[0].message.content
        return message_text
    except Exception as e:
        print(f"Erro ao se comunicar com a OpenAI: {e}")
        return None

def salvar_texto_em_diretorio(texto, tema, diretorio="teacher_texts"):
    """
    Salva o texto gerado em um arquivo dentro do diretório especificado.
    O nome do arquivo é baseado no tema, com espaços substituídos por underscores.
    """

    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    

    nome_arquivo = f"{tema.lower().replace(' ', '_')}.txt"
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(texto)
    
    return caminho_arquivo

if __name__ == "__main__":

    try:
        carregar_configuracoes()
    except ValueError as ve:
        print(ve)
        exit(1)


    temas = ler_tempos_json()


    tema = buscar_e_atualizar_primeiro_tema(temas)
    
    if tema is None:
        print("Todos os temas já foram executados.")
    else:
        print(f"Tema selecionado: {tema}")

        salvar_tempos_json(temas)


        texto_aula = gerar_texto_aula(tema)
        if texto_aula:
            print("Texto gerado pela OpenAI:")
            print(texto_aula)
            

            caminho_salvo = salvar_texto_em_diretorio(texto_aula, tema)
            print(f"Texto salvo em: {caminho_salvo}")
        else:
            print("Não foi possível gerar o texto da aula.")