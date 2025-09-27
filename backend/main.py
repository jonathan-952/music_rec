from fastapi import FastAPI
import model
import db
import pandas as pd
from contextlib import asynccontextmanager
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

agent = ''
retreival = ''
sp = ''
app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    connect = db.connection()
    cur = connect.cursor()


    df = pd.DataFrame(db.get_all())
    context_df = df.drop(columns = df.columns[[0, 8, 9, 10, 11, 12]])

    mp3_files = db.get_mp3()

    agent = model.ThompsonSampling(7)
    retreival = model.Retreival(df, context_df, mp3_files)

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id= os.getenv("CLIENT_ID"),
    client_secret= os.getenv("CLIENT_SECRET")
    ))

    yield



app.get('/recommend-song')
async def recommend():
    # this should return the index of mp3 file, fetch from db and play on frontend
    return retreival.recommendation(agent, sp)

app.post('/feedback')
async def feedback(index, rating):
    retreival.handle_update(index, rating, agent)

app.get('/liked-songs')
async def get_liked_songs():
    return retreival.liked_songs()
    
    
    






    


    

    


    
    



    
