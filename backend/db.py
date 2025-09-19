import psycopg2
import os
from dotenv import load_dotenv
from annoy import AnnoyIndex
import numpy as np
import pandas as pd


def connection():
    load_dotenv()

    username = os.getenv("DB_USERNAME")
    pwd = os.getenv("DB_PASSWORD")

    connection = psycopg2.connect(
        host = "localhost",
        database = "postgres",
        port=15432, 
        user = username,
        password = pwd
    )

    return connection

def get_all(cur):
    cur.execute("""
    SELECT * FROM songs
    """)

    data = cur.fetchall()
    return data
    
    return df

