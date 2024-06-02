import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

# Load the dataset
data = pd.read_csv('data/trackdata.csv')

# Define the columns to include for clustering
columns_to_include = [
    'danceability', 'energy', 'key', 'loudness', 'mode',
    'speechiness', 'acousticness', 'instrumentalness', 'liveness',
    'valence', 'tempo', 'time_signature'
]

data_for_clustering = data[columns_to_include]
Z = linkage(data_for_clustering, method='complete')

num_clusters = 4
clusters = fcluster(Z, num_clusters, criterion='maxclust')
data['cluster'] = clusters

# Sort the DataFrame by the 'cluster' column
data_sorted = data.sort_values(by='cluster')
data_sorted.to_csv('data/clustered_tracks.csv', index=False)

# Plot the dendrogram
plt.figure(figsize=(12, 6))
dendrogram(Z, p=45, truncate_mode='lastp', show_leaf_counts=True)
plt.xlabel('Data Points')
plt.ylabel('Distance')
plt.title('Hierarchical Clustering Dendrogram with 3 Clusters')
plt.show()
