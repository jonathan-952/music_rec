import csv
import os
from dotenv import load_dotenv
import db
from huggingface_hub import login
import kagglehub
from datasets import load_dataset, DatasetDict
import glob, shutil



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


def upload_mp3_files():
    load_dotenv()

    path = ""
    try:
        path = kagglehub.dataset_download("noahbadoa/fma-dataset-100k-music-wav-files")
    except Exception as e:
        print("Error:", e)

  
    target_path = os.path.join(path, "fma_large")

    all_mp3s = glob.glob(os.path.join(target_path, "**", "*.mp3"), recursive=True)
    flat_dir = os.path.join(path, "flat_mp3s")
    os.makedirs(flat_dir, exist_ok=True)

    for mp3 in all_mp3s:
        shutil.copy(mp3, flat_dir) 

    # files = glob.glob(path + r'\**\*.mp3', recursive = True)
    try: 
        dataset = load_dataset("audiofolder", data_dir=target_path)

        dataset_small = dataset["train"].select(range(100))
        print(len(dataset_small))
        login(token=os.getenv("HF_TOKEN"))
        dataset_small.push_to_hub("johnpork12345/music")
    except Exception as e:
        print(e)
    else:
        print('successful')
    
upload_mp3_files()


