import os
import psycopg2
from dotenv import load_dotenv
import requests
import json
import datetime
from datetime import date


load_dotenv()

DB_USER     = os.getenv('DB_USER')
DB_HOST     = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_TABLE    = os.getenv('DB_TABLE')
TOKEN       = os.getenv('TOKEN')

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

def make_request_sub_info(id,token):
    url = f"https://api.iugu.com/v1/subscriptions/{id}?api_token={token}"
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    return response_json

conect  = conectando_bd(DB_TABLE,DB_USER,DB_PASSWORD)
cur     = conect.cursor()

token   = TOKEN

query   = """
    SELECT
        "ID_ASSINATURA"
        ,"STATUS_ASSINATURA"
    FROM receita_contratada AS rc

    WHERE rc."PLATAFORMA_VENDA" = 'iugu'

    """

cur.execute(query)

base = cur.fetchall()
for b in base:
    id = b[0]
    status = b[1]
    
    dados = make_request_sub_info(token,id)
    
    try:
        data_atualizacao = dados['updated_at']
        data_atualizacao_obj = datetime.datetime.strptime(data_atualizacao, '%Y-%m-%dT%H:%M:%S%z')
        data = data_atualizacao_obj.strftime('%Y-%m-%d')
    except:
        data_1 = '1900-01-01'
        data = data_1
    data_atual = date.today()
    data_hoje = data_atual.strftime('%Y-%m-%d') 
    

    
    insert_query_log = """
        INSERT INTO log_assinaturas (
        "ID_ASSINATURA"
        ,"STATUSANT"
        ,"DATA_ATUALIZACAO"
        ,"DATA_ATUALIZACAO_SITE"
    ) VALUES (%s,%s,%s,%s)
    """

    dados = (
        id
        ,status
        ,data_hoje
        ,data
    )
    cur.execute(insert_query_log,dados)
    
    conect.commit()

    print(id)



