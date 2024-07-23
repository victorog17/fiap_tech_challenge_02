from aws_utils import handle_s3
import os

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# handle_s3(file_name, bucket, access_key, secret_key, action, object_name=None, prefix=None)

# Exemplo de uso para upload:
handle_s3(r"C:\Users\Victor_1\Documents\VSCode\fiap_tech_challenge_02\src\ibov_atual.csv",  # Corrigido
          'victor-mlet-tech-challenge-02', # Apenas o nome do bucket
          aws_access_key_id,
          aws_secret_access_key,
          'upload',
          'ibov_atual.csv', # Caminho no S3 onde o arquivo será salvo
          'raw')

# Instrução para salvar arquivo em parquet
# https://stackoverflow.com/questions/41066582/python-save-pandas-data-frame-to-parquet-file