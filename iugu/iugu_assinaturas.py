import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_USER     = os.getenv('DB_USER')
DB_HOST     = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_TABLE    = os.getenv('DB_TABLE')

# Função para conectar no banco de dados
def conectando_bd(DB_TABLE,DB_USER,DB_PASSWORD,DB_HOST):
    conn = psycopg2.connect(
        dbname=DB_TABLE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

    # Criando um cursor

    return conn