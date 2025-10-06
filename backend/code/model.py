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
            mask = np.array([g in self.seen for g in annoy])
            # np fancy indexing
            scores[mask] = -np.inf

        # return index of vector in our dataframe
        return np.argmax(scores)

    def update(self, rec_vector, reward, seen_song):

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

        for index in self.feedback.values():
            song = self.metadata.iloc[index]
            liked.append({
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
            # fallback: random seed if no feedback yet
            centroid = self.context_df.sample(1).to_numpy().flatten()
        
        annoy_indices = self.annoy.get_nns_by_vector(centroid, 5, search_k=len(self.context_df))

        candidates = self.context_df.iloc[annoy_indices]
        # full metadata df
        df_2 = self.metadata.iloc[annoy_indices]
        # map indices to embeddings in context df
        rec_song_index = agent.select_arm(candidates.to_numpy(), annoy_indices)

        
        global_index = annoy_indices[rec_song_index]
        # audio_file_index = self.metadata.iloc[global_index, 12]
        
        title = self.metadata.loc[global_index, 8]
        artist = self.metadata.loc[global_index, 9]
 
        query = f"{title} {artist}"
        rec_audio = self.get_audio(query, sp)
        print(rec_audio)

        return {'index': global_index, 'audio': rec_audio, 'artist': artist, 'title': title}
        
        
    # logic to get feedback from user and update
    def handle_update(self, index, reward, agent):
        self.feedback[index] = reward
        
        context_vector = self.context_df.iloc[index].to_numpy()
        
        agent.update(context_vector, reward, index)
    
    def get_audio(self, query, sp):
        res = sp.search(q=query, type="track", limit=1)
        print(res["tracks"]["items"][0])
        return res["tracks"]["items"][0]['preview_url']

        
    