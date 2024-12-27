import os
import json
from datetime import datetime
from dotenv import load_dotenv
import openai
from elevenlabs import generate, save

# Carregar variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Definir os dados dos estudantes
estudantes = {
    "Gabriel": "+34674804376",
    "Bruno": "+5511982864581"
}

temas = [
    "saudações e despedidas",
    "dias da semana e meses do ano",
    "cores e formas",
    "números e contagem",
    "palavras de família e parentesco",
    "ações do dia a dia (verbos básicos)",
    "comida e bebida",
    "lugares na cidade",
    "adjetivos comuns",
    "clima e tempo",
]


def obter_tema_do_dia():
    dia = datetime.now().day
    return temas[dia % len(temas)]  


def gerar_texto_aula(tema):
    prompt = f"o seu nome e Greta Crie uma lição simples de alemão para iniciantes, focando no tema '{tema}'. Inclua exemplos práticos e palavras básicas."
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()




def gerar_audio(texto, output_path):
    audio = generate(
        text=texto,
        voice="Arnold",  
        model="eleven_monolingual_v1"
    )
    save(audio, output_path)


def salvar_transcricao(estudante, texto):

    diretorio = "aulas"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)


    data_atual = datetime.now().strftime("%Y-%m-%d")
    arquivo_json = os.path.join(diretorio, f"{data_atual}.json")


    historico = {}
    if os.path.exists(arquivo_json):
        with open(arquivo_json, "r") as arquivo:
            historico = json.load(arquivo)


    if estudante not in historico:
        historico[estudante] = []
    historico[estudante].append({
        "data": datetime.now().isoformat(),
        "conteudo": texto
    })


    with open(arquivo_json, "w") as arquivo:
        json.dump(historico, arquivo, indent=4, ensure_ascii=False)

    print(f"Transcrição salva no arquivo {arquivo_json}.")


if __name__ == "__main__":

    tema_do_dia = obter_tema_do_dia()
    print(f"Tema do dia: {tema_do_dia}")

    prompt = "o seu nome e Greta e voce e professora de alemao.Crie uma lição simples de alemão para iniciantes, focando em saudações e palavras básicas."


    for estudante, numero in estudantes.items():
        print(f"Gerando lição para {estudante}...")


        texto_gerado = gerar_texto_aula(prompt)
        print(f"Texto gerado para {estudante}: {texto_gerado}")


        audio_path = f"licao_{estudante}.mp3"
        gerar_audio(texto_gerado, audio_path)
        print(f"Áudio gerado para {estudante} em {audio_path}")


        salvar_transcricao(estudante, texto_gerado)