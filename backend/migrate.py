import csv
import os
from dotenv import load_dotenv
import db
import boto3


def upload_csv():
    connect = db.connection()
    cur = connect.cursor()

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

    connect.commit()
    cur.close()
    connect.close()


# def upload_mp3_files():
#     path = ""
#     try:
#         path = kagglehub.dataset_download("noahbadoa/fma-dataset-100k-music-wav-files")
#     except Exception as e:
#         print("Error:", e)

#     target_path = path + r'\fma_large'
#     files = glob.glob(path + r'\**\*.mp3', recursive = True)

#     obj = boto3.client("s3")
#     for i in range(len(files)):

#         obj.upload_file(
#             Filename= files[i],
#             Bucket="songrecaudio",
#             Key= f"{i}"
#         )

