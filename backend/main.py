from fastapi import FastAPI
import model
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

    mp3_files = db.get_mp3()
    

    agent = model.ThompsonSampling(7)
    retreival = model.Retreival(df, context_df, mp3_files)

    yield

app.get('/get-audio')
async def get_audio(song_index: int):
    # load mp3 file to listen to
    #  HF API request

app.get('/recommend-song')
async def recommend():
    # this should return the index of mp3 file, fetch from db and play on frontend
    song = retreival.recommendation()

app.post('/feedback')
async def feedback(index, rating):
    retreival.handle_update(index, rating, agent)

app.get('/liked-songs')
async def 
    
    






    


    

    


    
    



    
