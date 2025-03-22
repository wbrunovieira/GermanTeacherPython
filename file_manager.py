import os
import re

def salvar_texto_em_diretorio(texto, tema, diretorio="teacher_texts"):
    """Salva o texto gerado em um arquivo."""
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    # Substitui caracteres inválidos por underline
    nome_arquivo = re.sub(r'[^\w\s-]', '', tema.lower())  # remove parênteses, barras, etc.
    nome_arquivo = nome_arquivo.replace(' ', '_') + ".txt"

    caminho_arquivo = os.path.join(diretorio, nome_arquivo)

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(texto)

    return caminho_arquivo