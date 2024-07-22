import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from unidecode import unidecode

def clean_column_name(column_name):
    """Remove acentos e caracteres especiais de um nome de coluna."""
    # Remove acentos
    column_name = unidecode(column_name)
    # Remove caracteres especiais, mantendo letras, números e underscores
    column_name = re.sub(r'\W+', '_', column_name)
    # Adiciona '_percentual' ao final se o nome da coluna termina com '_'
    if column_name.endswith('_'):
        column_name += 'percentual'
    return column_name

def download_latest_csv(indice, tempo=2):
    """Faz o download do arquivo CSV mais recente da página do índice especificado."""
    options = Options()
    
    # Define o diretório atual como o diretório de download
    current_directory = os.getcwd()
    prefs = {'download.default_directory': current_directory}
    options.add_experimental_option('prefs', prefs)

    # Inicializa o WebDriver com as opções configuradas
    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Acessa a URL do índice
    url = f'https://sistemaswebb3-listados.b3.com.br/indexPage/day/{indice.lower()}?language=pt-br'
    wd.get(url)
    time.sleep(tempo)  # Espera para garantir que a página carregue completamente
    
    # Encontra a caixa de pesquisa e envia o texto "Setor de Atuação"
    search_box = wd.find_element(By.ID, "segment")
    search_box.send_keys("Setor de Atuação")
    time.sleep(tempo)  # Espera para garantir que a interação ocorra

    # Encontra e clica no link de download
    search_link_download = wd.find_element(By.LINK_TEXT, "Download")
    search_link_download.click()
    
    time.sleep(tempo)  # Espera para garantir que o download seja concluído
    wd.quit()  # Encerra o WebDriver

def get_csv_files(directory='.'):
    """Retorna uma lista de arquivos CSV no diretório especificado."""
    return [f for f in os.listdir(directory) if f.endswith('.csv')]

def get_latest_file(files):
    """Retorna o arquivo mais recentemente modificado de uma lista de arquivos."""
    if not files:
        return None
    return max(files, key=lambda f: os.path.getmtime(f))

def main(indice):
    """Função principal para baixar o CSV mais recente, renomear colunas e exibir o DataFrame."""
    download_latest_csv(indice, tempo=10)

    # Obtém a lista de arquivos CSV no diretório atual
    csv_files = get_csv_files()
    if not csv_files:
        print("Não há arquivos CSV no diretório.")
        return
    
    # Obtém o arquivo CSV mais recente
    latest_file = get_latest_file(csv_files)
    if latest_file:
        print(f"O arquivo CSV mais recente é: {latest_file}")
        
        # Lê o arquivo CSV usando pandas com as configurações especificadas
        df = pd.read_csv(latest_file, sep=';', encoding='ISO-8859-1', skipfooter=2, engine='python', thousands='.', decimal=',', header=1, index_col=False)
        
        # Renomeia as colunas utilizando clean_column_name
        df = df.rename(columns=clean_column_name)

        # Salva o CSV já limpo
        df.to_csv("../src/ibov_atual.csv", sep=';', index=False, encoding='UTF-8')
        
        # Exibe o DataFrame com os nomes das colunas atualizados
        print(df)
    else:
        print("Não foi possível encontrar o arquivo CSV mais recente.")

# Exemplo de chamada da função principal
if __name__ == "__main__":
    main('ibov')
