from fastapi import FastAPI
from . import model
from . import db
import pandas as pd
from contextlib import asynccontextmanager
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class FeedbackModel(BaseModel):
    rating: int
    index: int

origins = [
        "http://localhost:3000",  # Example: your frontend development server
        # Example: your deployed frontend
        # You can add more origins as needed
    ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent, retreival, sp
    load_dotenv()
    connect = db.connection()
    cur = connect.cursor()


    df = pd.DataFrame(db.get_all(cur))
    context_df = df.drop(columns = df.columns[[0, 8, 9, 10, 11, 12]])


    agent = model.ThompsonSampling(7)
    retreival = model.Retreival(df, context_df)

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id= os.getenv("CLIENT_ID"),
    client_secret= os.getenv("CLIENT_SECRET")
    ))

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,  # Allow cookies to be sent with requests
        allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],     # Allow all headers
    )

@app.get('/recommend-song')
async def recommend():
    # this should return the index of mp3 file, fetch from db and play on frontend
    return retreival.recommendation(agent, sp)

@app.post('/feedback')
async def feedback(req: FeedbackModel):
    retreival.handle_update(req.index, req.rating, agent)

@app.get('/liked-songs')
async def get_liked_songs():
    return retreival.liked_songs()
    
    
    






    


    

    


    
    



    
