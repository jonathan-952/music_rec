from fastapi import FastAPI
import main
# REQUIREMENTS:
# take in user response (like, dislike)
# upload csv and mp3 files
# load mp3 file to listen to
# load other metadata
#  compute centroid
# 
app = FastAPI()


feedback = {}


# data frame
# df = pd.read_csv('featuresV2.csv')
context_df = df.drop(columns = df.columns[[0, 8, 9, 10, 11, 12]])

annoy_index = main.build_annoy(context_df)

agent = main.ThompsonSampling(7)

@app.on_event('startup')
async def load_cache():
    
