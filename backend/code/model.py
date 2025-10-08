from sklearn.neighbors import NearestNeighbors as nn 
import pandas as pd
import numpy as np 
import glob
from annoy import AnnoyIndex
from . import db



class ThompsonSampling:
    def __init__(self, features):
        self.features = features
        self.mu = np.zeros(features)
        self.sigma = np.identity(features)
        self.seen = set()


    def sample(self):
        return np.random.multivariate_normal(self.mu, self.sigma)

    def select_arm(self, contexts, annoy): 
        
        theta = self.sample()

        scores = contexts @ theta

        if self.seen:
            # create boolean mask of seen indices
            mask = np.isin(annoy, list(self.seen))
            # np fancy indexing
            scores[mask] = -np.inf

        # return index of vector in our dataframe
        return np.argmax(scores)

    def update(self, rec_vector, reward, seen_song):
        # need to pass in rec_vector
        rec_vector = rec_vector.reshape(1, -1)

        sigma_inv = np.linalg.inv(self.sigma)
        self.sigma = np.linalg.inv(sigma_inv + rec_vector @ rec_vector.T)

        self.mu = self.sigma @ (sigma_inv @ self.mu + reward * rec_vector.flatten())

        self.seen.add(seen_song)



class Retreival:
    def __init__(self, metadata, context_df):
        self.context_df = context_df
        self.metadata = metadata
        self.annoy = self.start_annoy(context_df)
        self.feedback = {}
    
    def start_annoy(self, context_df):
        t = AnnoyIndex(7, 'angular')

        arr = context_df.to_numpy()
        for i, v in enumerate(arr):
            t.add_item(i, v)

        t.build(10) # 10 trees
        u = t

        return u
    
    def liked_songs(self):
        liked = []

        for index, value in self.feedback.items():
            song = self.metadata.iloc[index]
            if value == 1:
                liked.append({
                    "id": int(index),
                    "artist" : song[9],
                    "title" : song[8]
                })

        return liked

    def compute_centroid(self):
        if not self.feedback:
            return None  # no feedback yet
        
        indices = list(self.feedback.keys())
        weights = np.array(list(self.feedback.values()))
        
        mask = weights != 0  # ignore skips
        embeddings = self.context_df.iloc[indices].to_numpy()
        
        numerator = np.sum(weights[mask, None] * embeddings[mask], axis=0)
        denominator = np.sum(np.abs(weights[mask]))
        
        return numerator / denominator if denominator > 0 else None

    def recommendation(self, agent, sp):
        centroid = self.compute_centroid()

        if centroid is None:
            centroid = self.context_df.sample(1).to_numpy().flatten()
        
        annoy_indices = self.annoy.get_nns_by_vector(centroid, 50, search_k=len(self.context_df))
        candidates = self.context_df.iloc[annoy_indices]
        df_2 = self.metadata.iloc[annoy_indices]

        tried = set()
        rec_audio = None
        rec_song_index = None
        global_index = None

        for _ in range(len(annoy_indices)):
            rec_song_index = agent.select_arm(candidates.to_numpy(), annoy_indices)
            global_index = annoy_indices[rec_song_index]

            title = self.metadata.loc[global_index, 8]
            artist = self.metadata.loc[global_index, 9]
            query = f"{title} {artist}"

            rec_audio = self.get_audio(query, sp)

            if rec_audio:
                break

            tried.add(global_index)

            # remove tried index from candidates and annoy_indices
            mask = ~candidates.index.isin(tried)
            candidates = candidates[mask]
            annoy_indices = annoy_indices[mask]

            if candidates.empty:
                rec_audio = 'https://www.youtube.com/watch?v=BIkUPiXVB18'
                break

        return {
            "index": int(global_index),
            "title": title,
            "artist": artist,
            "audio": rec_audio
        }  
        
    # logic to get feedback from user and update
    def handle_update(self, index, reward, agent):
        self.feedback[index] = reward
        
        context_vector = self.context_df.iloc[index].to_numpy()
        
        agent.update(context_vector, reward, index)
    
    def get_audio(self, query, yt):
        request = yt.search().list(
            part="snippet",
            q= query,
            type="video",
            maxResults=5
        )
        response = request.execute()

        for item in response["items"]:
            video_id = item["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"

            if video_id:
                return url
        
        return None
        


        
    