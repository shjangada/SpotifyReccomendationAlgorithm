from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np


# Load the dataset
data = pd.read_csv('data/trackdata.csv')

# Define the columns to include for clustering
columns_to_include = [
    'danceability', 'energy', 'key', 'loudness', 'mode',
    'speechiness', 'acousticness', 'instrumentalness', 'liveness',
    'valence', 'tempo', 'duration_ms', 'time_signature'
]

# Extract the data to be used for clustering
data_for_clustering = data[columns_to_include]

# Initialize DBSCAN with appropriate parameters
dbscan = DBSCAN(eps=4000, min_samples=5)
labels = dbscan.fit_predict(data_for_clustering)

# Create a dictionary to store the mapping of cluster labels to lists of song URIs
song_uris = data['uri']
cluster_song_mapping = {}

for song_uri, cluster_label in zip(song_uris, labels):
    if cluster_label not in cluster_song_mapping:
        cluster_song_mapping[cluster_label] = []
    cluster_song_mapping[cluster_label].append(song_uri)

print("Cluster Label Song URI Mapping:", cluster_song_mapping)

# Reduce the dimensions to 2D using PCA
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(data_for_clustering)
plt.figure(figsize=(10, 8))

unique_labels = set(labels)
for label in unique_labels:
    if label == -1:
        # Outliers
        cluster_points = reduced_data[labels == label]
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label='Outliers', alpha=0.5, color='black')
    else:
        cluster_points = reduced_data[labels == label]
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {label}', alpha=0.5)

plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('Clusters of Tracks')
plt.legend()
plt.show()
