#This method takes exemplars from both the center and outliers, but for reccomendations it makes more sense to take tracks that are in the center.

from sklearn.cluster import AffinityPropagation
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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

# Initialize and fit the AffinityPropagation model
ap = AffinityPropagation()
ap.fit(data_for_clustering)

# Get the cluster labels and exemplars
labels = ap.labels_
exemplars = ap.cluster_centers_indices_

# Create a DataFrame with the original data and the cluster labels
clustered_data = data.copy()
clustered_data['Cluster'] = labels

# Print the exemplars
print("Exemplars:")
print(data.iloc[exemplars])

# If you need the actual tracks for further use, you can access them like this:
exemplar_tracks = data.iloc[exemplars]


# Reduce the dimensions to 2D using PCA
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(data_for_clustering)

# Create a scatter plot of the reduced data
plt.figure(figsize=(10, 8))

# Use the cluster labels to color the points
for cluster_id in np.unique(labels):
    cluster_points = reduced_data[labels == cluster_id]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {cluster_id}', alpha=0.5)

# Highlight the exemplars
exemplar_points = reduced_data[exemplars]
plt.scatter(exemplar_points[:, 0], exemplar_points[:, 1], color='red', marker='x', s=100, label='Exemplars')

plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('Clusters of Tracks')
plt.legend()
plt.show()