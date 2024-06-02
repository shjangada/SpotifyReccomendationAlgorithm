import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('data/trackdata.csv')

# Define the columns to include for clustering
columns_to_include = [
    'danceability', 'energy', 'key', 'loudness', 'mode',
    'speechiness', 'acousticness', 'instrumentalness', 'liveness',
    'valence', 'tempo', 'time_signature'
]

# Extract the data to be used for analysis
data_for_analysis = data[columns_to_include]

# Generate random binary target labels for the sake of this example
target = np.random.randint(0, 2, size=data_for_analysis.shape[0])

# Initialize and fit the Gradient Boosting model
model = GradientBoostingClassifier()
model.fit(data_for_analysis, target)

# Get feature importances
feature_importances = model.feature_importances_

# Create a DataFrame for better visualization
importance_df = pd.DataFrame({'Feature': columns_to_include, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Plot feature importances
plt.figure(figsize=(12, 6))
sns.barplot(x='Importance', y='Feature', data=importance_df)
plt.title('Feature Importance from Gradient Boosting')
plt.show()

# Select the top N important features
top_features = importance_df.head(5)['Feature'].values

print("Top features to use for recommendations:", top_features)
