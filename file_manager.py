import os

def salvar_texto_em_diretorio(texto, tema, diretorio="teacher_texts"):
    """Salva o texto gerado em um arquivo."""
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    nome_arquivo = f"{tema.lower().replace(' ', '_')}.txt"
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(texto)
    
    return caminho_arquivo