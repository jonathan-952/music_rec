from sklearn.neighbors import NearestNeighbors as nn 
import pandas as pd
import numpy as np 
import glob
import IPython.display as ipt
import librosa
import kagglehub
from annoy import AnnoyIndex


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

feedback = {}

def compute_centroid(context_df, feedback):
    if not feedback:
        return None  # no feedback yet
    
    indices = list(feedback.keys())
    weights = np.array(list(feedback.values()))
    
    mask = weights != 0  # ignore skips
    embeddings = context_df.iloc[indices].to_numpy()
    
    numerator = np.sum(weights[mask, None] * embeddings[mask], axis=0)
    denominator = np.sum(np.abs(weights[mask]))
    
    return numerator / denominator if denominator > 0 else None
    
# data frame
df = pd.read_csv('featuresV2.csv')
context_df = df.drop(columns = df.columns[[0, 8, 9, 10, 11, 12]])

# ANNOY
def buildAnnoy():

    t = AnnoyIndex(7, 'angular')
    for i in range(len(context_df.to_numpy())):
        v = context_df.iloc[i]
        t.add_item(i, v)

    t.build(10) # 10 trees
    u = t

    return u


agent = ThompsonSampling(7)


for i in range(1000):
    centroid = compute_centroid(context_df, feedback)

    if centroid is None:
        # fallback: random seed if no feedback yet
        centroid = context_df.sample(1).to_numpy().flatten()
    
    build_annoy = buildAnnoy()
    annoy_indices = build_annoy.get_nns_by_vector(centroid, 5, search_k=len(context_df))

    candidates = context_df.iloc[annoy_indices]
    # full metadata df
    df_2 = df.iloc[annoy_indices]
    # map indices to embeddings in context df
    rec_song_index = agent.select_arm(candidates.to_numpy(), annoy_indices)

    
    global_index = annoy_indices[rec_song_index]
    audio_file_index = df.iloc[global_index, 12]
    rec_vector = files[audio_file_index]
    
    y, sr = librosa.load(rec_vector, sr=22050)
    display(ipt.Audio(data=y, rate=sr))
    
    reward = int(input('Like: 1, Dislike: -1 ;'))
 
    feedback[global_index] = reward
    
    context_vector = context_df.iloc[global_index].to_numpy()
    
    agent.update(context_vector, reward, global_index)