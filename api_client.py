import openai

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
                    "Escreva o texto de forma amigável, com no mínimo 500 caracteres e no máximo 1000 caracteres."
                )}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro na comunicação com a Deepseek: {e}")
        return None