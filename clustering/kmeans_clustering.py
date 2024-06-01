#This method still creates clusters of outliers and one of the centroids becomes an outlier
#Trying DBSCAN next to skip over the outliers

import pandas as pd
from sklearn.cluster import KMeans
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

# Initialize and fit the KMeans model
n_clusters = 6  # Played around with this number until it didn't accept too many outliers but was enough to be meaningful
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(data_for_clustering)

# Get the cluster labels and centroids
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

# Create a DataFrame with the original data and the cluster labels
clustered_data = data.copy()
clustered_data['Cluster'] = labels

# Reduce the dimensions to 2D using PCA
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(data_for_clustering)
reduced_centroids = pca.transform(centroids)

# Create a scatter plot of the reduced data
plt.figure(figsize=(10, 8))

# Use the cluster labels to color the points
for cluster_id in range(n_clusters):
    cluster_points = reduced_data[labels == cluster_id]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {cluster_id}', alpha=0.5)

# Highlight the centroids
plt.scatter(reduced_centroids[:, 0], reduced_centroids[:, 1], color='red', marker='x', s=100, label='Centroids')

plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('Clusters of Tracks')
plt.legend()
plt.show()

# If you need the actual tracks for further use, you can access the centroids like this:
centroid_tracks = pd.DataFrame(centroids, columns=columns_to_include)
print("Centroids:")
print(centroid_tracks)
