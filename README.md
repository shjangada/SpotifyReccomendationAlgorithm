# Spotify Recommendation Algorithm

## Overview
This project aims to develop a recommendation algorithm for Spotify users based on their listening history and preferences. The algorithm utilizes audio features of songs to evaluate and recommend tracks that align with the user's tastes.

## Usage

### Step 1: Data Collection
- **Get User's Top Tracks**: Gather the user's top tracks over the last 6 months to train the model on liked songs.
- **Select Neutral/Disliked Songs**: Collect songs ranked between 75 - 125 in the user's listening history over the last 6 months to train the model on neutral/disliked songs.

### Step 2: Search and Database Creation
- **Search by Artists and Genres**: Due to limitations in searching Spotify's entire database, search is based on the user's top artists and genres.
- **Database Creation**: Compile a database with 20 songs per artist and per genre, using data collected from followed artists, top artists, and associated genres.

### Step 3: Algorithm Application
- **Machine Learning Algorithms**: Explore various algorithms for recommendation:
    - **Logistic Regression**: Found to be the most effective algorithm for recommendation, located in the project folder.
    - **AP Cluster**: Utilizes exemplars from both the center and outliers, but refinement is needed for better recommendation selection.
    - **DBSCAN Clustering**: Generates clusters without preset parameters, requiring further optimization.
    - **Hierarchical Clustering**: Provides insight into song similarities and cluster convergence but needs refinement for cluster quantity and shape.
    - **K-means**: Tends to create clusters of outliers, requiring adjustments to centroid selection.

### Step 4: Evaluation and Improvement
- **Gradient Boosting**: Explored for feature importance understanding but lacks a set target for supervised learning.
- **Iterative Refinement**: Continuously refine algorithms based on performance and user feedback.


## Issues
- **Clustering Challenges**: Addressing issues with clustering algorithms to optimize cluster selection for recommendation accuracy.
- **Supervised Learning Limitation**: Lack of a set target inhibits the use of supervised learning techniques.
- **Algorithmic Refinement**: Ongoing process of fine-tuning algorithms to improve recommendation precision and relevance.

