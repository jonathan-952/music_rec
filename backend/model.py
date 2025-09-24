from sklearn.neighbors import NearestNeighbors as nn 
import pandas as pd
import numpy as np 
import glob
import IPython.display as ipt
import librosa
from annoy import AnnoyIndex
import db


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
    def __init__(self, metadata, context_df, mp3_files):
        self.context_df = context_df
        self.metadata = metadata
        self.annoy = self.start_annoy()
        self.feedback = {}
        self.mp3_files = db.get_mp3()
    
    async def start_annoy(self, context_df):
        t = AnnoyIndex(7, 'angular')
        for i in range(len(self.context_df.to_numpy())):
            v = context_df.iloc[i]
            t.add_item(i, v)

        t.build(10) # 10 trees
        u = t

        return u

    def compute_centroid(self, feedback):
        if not feedback:
            return None  # no feedback yet
        
        indices = list(feedback.keys())
        weights = np.array(list(feedback.values()))
        
        mask = weights != 0  # ignore skips
        embeddings = self.context_df.iloc[indices].to_numpy()
        
        numerator = np.sum(weights[mask, None] * embeddings[mask], axis=0)
        denominator = np.sum(np.abs(weights[mask]))
        
        return numerator / denominator if denominator > 0 else None

    def recommendation(self, agent):
        centroid = self.compute_centroid(self.context_df, self.feedback)

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
        audio_file_index = self.metadata.iloc[global_index, 12]
        title = self.metadata.iloc[global_index, 'title']
        artist = self.metadata.iloc[global_index, 'artist']
        # call HF API eventually
        rec_audio = self.mp3_files[audio_file_index]

        return {'index': global_index, 'audio': rec_audio, 'artist': artist, 'title': title}
        

        # send mp3 file as response, along with global index to store on fe before sending back to be to update

        
    # logic to get feedback from user and update
    def handle_update(self, index, reward, agent):
        self.feedback[index] = reward
        
        context_vector = self.context_df.iloc[index].to_numpy()
        
        agent.update(context_vector, reward, index)
        
    