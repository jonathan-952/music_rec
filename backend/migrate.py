import psycopg2
import csv
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("DB_USERNAME")
pwd = os.getenv("DB_PASSWORD")

connection = psycopg2.connect(
    host = "db-music.cy9gckmqm7nz.us-east-1.rds.amazonaws.com",
    database = "db-music",
    user = username,
    password = pwd
)

cur = connection.cursor()

cur.execute("""
    CREATE TABLE songs (
        id SERIAL PRIMARY KEY,
        mfcc_mean FLOAT,
        mfcc_std FLOAT,
        tempo FLOAT,
        spec_centroid_mean FLOAT,
        spec_rolloff_mean FLOAT,
        chroma_mean FLOAT
        zero_crossing_mean FLOAT
        title TEXT,
        artist TEXT,
        genre TEXT
            )
            """)

with open("..testing/features.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header row

    for row in reader:
        # Drop last column (extra_column)
        row = row[:-1]  

        cur.execute(
            "INSERT INTO songs (,mfcc_mean,mfcc_std,tempo,spec_centroid_mean,spec_rolloff_mean,chroma_mean,zero_crossing_mean,title,artist,genre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            row
        )

connection.commit()
cur.close()
connection.close()