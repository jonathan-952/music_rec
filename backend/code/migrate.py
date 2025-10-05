import csv
import os
from dotenv import load_dotenv
import backend.code.db as db
from huggingface_hub import login
import kagglehub
from datasets import load_dataset, DatasetDict
import glob, shutil
import soundfile as sf


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


def upload_mp3_files(sample_size=200):
    load_dotenv()
    try:
        path = kagglehub.dataset_download("noahbadoa/fma-dataset-100k-music-wav-files")
    except Exception as e:
        print("Error downloading dataset:", e); return

    all_mp3s = glob.glob(os.path.join(path, "fma_large", "**", "*.mp3"), recursive=True)
    print("Found", len(all_mp3s), "mp3 files")

    subset_mp3s = all_mp3s[:sample_size]

    flat_dir = os.path.join(path, "flat_mp3s")
    shutil.rmtree(flat_dir, ignore_errors=True)
    os.makedirs(flat_dir)

    def is_valid_audio(f):
        try:
            with sf.SoundFile(f) as s: s.read(frames=1)
            return True
        except: return False

    for f in subset_mp3s:
        if is_valid_audio(f):
            shutil.copy(f, flat_dir)

    try:
        dataset = load_dataset("audiofolder", data_dir=flat_dir, split="train", drop_labels=True)
        dataset_small = dataset.select(range(min(10, len(dataset))))
        login(token=os.getenv("HF_TOKEN"))
        dataset_small.push_to_hub("johnpork12345/music")
    except Exception as e:
        print("Error during dataset processing:", e)
    else:
        print('successful')



