import psycopg2
import csv
import os
from dotenv import load_dotenv

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

cur = connection.cursor()

# create table in db
cur.execute("""
    CREATE TABLE songs (
        id SERIAL PRIMARY KEY,
        mfcc_mean FLOAT,
        mfcc_std FLOAT,
        tempo FLOAT,
        spec_centroid_mean FLOAT,
        spec_rolloff_mean FLOAT,
        chroma_mean FLOAT,
        zero_crossing_mean FLOAT,
        title TEXT,
        artist TEXT,
        genre TEXT,
        duration FLOAT,
        index INT
            )
            """)

with open("../testing/featuresV2.csv", "r", encoding="utf-8") as f:
    cur.copy_expert(
        """
        COPY songs (id, mfcc_mean, mfcc_std, tempo, spec_centroid_mean, 
                    spec_rolloff_mean, chroma_mean, zero_crossing_mean, 
                    title, artist, genre, duration, index)
        FROM STDIN WITH CSV HEADER
        """,
        f
    )

connection.commit()
cur.close()
connection.close()