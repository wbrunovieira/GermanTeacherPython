# data_handler.py
import json
from datetime import datetime
import os
import time
from urllib.parse import urlparse

import requests

def ler_tempos_json(caminho='temas.json'):
    """Lê o arquivo JSON contendo os temas."""
    with open(caminho, 'r', encoding='utf-8') as file:
        return json.load(file)

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

