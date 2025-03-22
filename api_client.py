import openai

def gerar_texto_aula(client, tema):
    """Gera o texto de aula utilizando a API da Deepseek."""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é uma professora de alemão chamada Greta. "
                        "Você é simpática, paciente e fala de maneira gentil, como se estivesse conversando com o aluno em um áudio. "
                        "Seu aluno é brasileiro, totalmente iniciante em alemão. "
                        "Você está guiando uma conversa, ensinando passo a passo de forma interativa e acessível."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Crie uma lição falada de alemão para iniciantes, com o tema '{tema}'. "
                        "Fale sempre em português, explicando palavras e frases em alemão, com a tradução imediata. "
                        "Apresente uma ou duas frases em alemão e peça para o aluno repetir em voz alta. "
                        "Depois, peça para ele gravar e enviar o áudio de volta com a repetição. "
                        "Diga que assim poderemos continuar a conversa sobre o tema. "
                        "Use um tom de voz acolhedor e didático, como se fosse uma tutora particular guiando passo a passo. "
                        "Não use formatações como asteriscos, listas, ou títulos. "
                        "A resposta deve ter entre 500 e 1000 caracteres e soar como uma conversa real e amigável."
                    )
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro na comunicação com a Deepseek: {e}")
        return None