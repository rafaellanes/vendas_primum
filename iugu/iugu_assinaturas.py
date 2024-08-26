import os
import psycopg2
from dotenv import load_dotenv
import requests
import json

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

conect = conectando_bd(DB_TABLE,DB_USER,DB_PASSWORD)

def make_request(start,dtfrom,dtto,token):
    url = f"https://api.iugu.com/v1/subscriptions?limit=100&start={start}&created_at_from={dtfrom}&created_at_to={dtto}&api_token={token}"
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    return response_json
