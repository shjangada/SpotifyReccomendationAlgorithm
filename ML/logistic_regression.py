import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset of liked songs
liked_data = pd.read_csv('data/trackdata.csv')
liked_data['like'] = 1

# Load the dataset of neutral songs
neutral_data = pd.read_csv('data/neutral.csv')
neutral_data['like'] = 0

combined_data = pd.concat([liked_data, neutral_data], ignore_index=True)

# Define the columns to include for logistic regression
columns_to_include = [
    'danceability', 'energy', 'speechiness', 'acousticness', 'liveness',
    'valence', 'tempo'
]

# Extract the data to be used for analysis
data_for_analysis = combined_data[columns_to_include]
target = combined_data['like']
X_train, X_test, y_train, y_test = train_test_split(data_for_analysis, target, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

coefficients = model.coef_[0]

# Create a DataFrame for better visualization
coefficients_df = pd.DataFrame({'Feature': columns_to_include, 'Coefficient': coefficients})
coefficients_df['Absolute Coefficient'] = coefficients_df['Coefficient'].abs()  # Absolute values for sorting
coefficients_df = coefficients_df.sort_values(by='Absolute Coefficient', ascending=False)

# Plot coefficients
plt.figure(figsize=(12, 6))
sns.barplot(x='Coefficient', y='Feature', data=coefficients_df)
plt.title('Feature Coefficients from Logistic Regression')

# Select the top N important features
top_features = coefficients_df.head(5)['Feature'].values
print("Top features to use for recommendations:", top_features)

song_data = pd.read_csv('data/songdatabase.csv')
data_for_analysis = song_data[columns_to_include]
song_data['predicted_likelihood'] = model.predict_proba(data_for_analysis)[:, 1]
threshold = 0.835  # Define a threshold to classify predictions
song_data['predicted_preference'] = np.where(song_data['predicted_likelihood'] >= threshold, 'like', 'dislike')

# Print the IDs and preferences of the songs the user is predicted to like
liked_songs = song_data[song_data['predicted_preference'] == 'like']
print(liked_songs[['id', 'predicted_preference']])
