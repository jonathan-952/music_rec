from fastapi import FastAPI
import main
import db
import pandas as pd
from contextlib import asynccontextmanager

agent = ''
retreival = ''
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect = db.connection()
    cur = connect.cursor()

    df = pd.DataFrame(db.get_all())
    context_df = df.drop(columns = df.columns[[0, 8, 9, 10, 11, 12]])
    

    agent = main.ThompsonSampling(7)
    retreival = main.Retreival(context_df)

    yield

app.get('/get_audio')
async def get_audio(song_index: int):
    # load mp3 file to listen to

app.get('/recommend_song')
async def recommend():
    # this should return the index of mp3 file, fetch from db and play on frontend
    mp3_index = retreival.recommendation()
    
    






    


    

    


    
    



    
