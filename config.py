# config.py
import os
from dotenv import load_dotenv

def carregar_configuracoes():
    """Carrega a chave da API da Deepseek do ambiente"""
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY") 
    
    if not api_key:
       
        raise ValueError("Variável DEEPSEEK_API_KEY não encontrada no .env")
    
    return api_key 