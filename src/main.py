import requests as requests
import bs4 as bs4
import urllib.request as urlilb
import re

url_base = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br'

response = requests.get(url_base)
#soup = bs4.BeautifulSoup(response.content, "html.parser")

print(response)


# Instrução para salvar arquivo em parquet
# https://stackoverflow.com/questions/41066582/python-save-pandas-data-frame-to-parquet-file