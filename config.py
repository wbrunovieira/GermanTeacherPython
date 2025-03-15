# config.py
import os
from dotenv import load_dotenv
import openai

def carregar_configuracoes():
    """
    Carrega as variáveis de ambiente e configura a chave da API do OpenAI.
    """
    load_dotenv()  # Carrega o conteúdo do .env
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("A variável de ambiente OPENAI_API_KEY não está definida.")
    openai.api_key = api_key