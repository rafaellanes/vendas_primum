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
DB_PASSWORD = os.getenv('DB_PASSOWORD')
DB_TABLE    = os.getenv('DB_TABLE')
TOKEN       = os.getenv('TOKEN')

def conectando_bd(database,username,password):
# Conectando ao banco de dados
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host="34.29.110.105"
    )

    # Criando um cursor

    return conn

def make_request_sub_info(token,id):
    url = f"https://api.iugu.com/v1/subscriptions/{id}?api_token={token}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    return response_json

# Credencias Banco de Dados
database='iugu'
username='rafael.lanes'
password='"ZMvekst|aIMrY@J'

# Banco de Dados (POSTGREESQL)

conect = conectando_bd(database,username,password)
cur = conect.cursor()

# Consulta sql para pegar quais assinaturas precisa atualizar
query = """
    SELECT
        rc."ID_ASSINATURA"
        ,"STATUS_ASSINATURA"
    FROM receita_contratada AS rc

    LEFT JOIN log_assinaturas_iugu as temp
        ON temp."ID_ASSINATURA" = rc."ID_ASSINATURA"

    WHERE rc."PLATAFORMA_VENDA" = 'iugu'
        AND temp."ID_ASSINATURA" IS NULL
    """

# Executar Consulta

cur.execute(query)

base = cur.fetchall()
token = TOKEN
for b in base:
    id = b[0]
    status = b[1]

    dados = make_request_sub_info(token,id)

    try:
        suspenso                = dados['suspended']
    except:
        suspenso = None
    try:
        ativo                   = dados['active']
    except:
        ativo = None
        
    try:
        data_atualizacao        = dados['updated_at']
        data_atualizacao_obj    = datetime.datetime.strptime(data_atualizacao, '%Y-%m-%dT%H:%M:%S%z')
        data                    = data_atualizacao_obj
    except:
        data_1 = '1900-01-01'
        data = data_1

    insert_query_log = """
        INSERT INTO log_assinaturas_iugu (
        "ID_ASSINATURA"
        ,"STATUS"
        ,"DATA_ATUALIZACAO"
        
    ) VALUES (%s,%s,%s)
    """

    dados = (
        id
        ,ativo
        ,data
    )
    cur.execute(insert_query_log,dados)
    
    conect.commit()
    print(f"{id} com data de atualização no dia {data}.")


conect.close()

