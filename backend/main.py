from fastapi import FastAPI
# REQUIREMENTS:
# take in user response (like, dislike)
# upload csv and mp3 files
# load mp3 file to listen to
# load other metadata
#  compute centroid
# 
app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'tyshi'}

@app.post('/import_csv')
async def user_feedback():


@app.on_event('startup')
async def load_cache():
    