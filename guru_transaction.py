import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_USER     = os.getenv('DB_USER')
DB_HOST     = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_TABLE    = os.getenv('DB_TABLE')