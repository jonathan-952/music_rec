import psycopg2
import os
from dotenv import load_dotenv
# from annoy import AnnoyIndex
import numpy as np
import pandas as pd
import glob
import kagglehub


def connection():
    load_dotenv()

    username = os.getenv("DB_USERNAME")
    pwd = os.getenv("DB_PASSWORD")

    connection = psycopg2.connect(
        host = "db-music.cy9gckmqm7nz.us-east-1.rds.amazonaws.com",
        database = "db-music",
        port=5432, 
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


def get_mp3():
    path = ""
    try:
        path = kagglehub.dataset_download("noahbadoa/fma-dataset-100k-music-wav-files")
    except Exception as e:
        print("Error:", e)

    target_path = path + r'\fma_large'
    files = glob.glob(path + r'\**\*.mp3', recursive = True)
    return files

