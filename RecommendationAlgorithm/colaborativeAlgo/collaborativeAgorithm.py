import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Sample user-item rating matrix
data = {
    'User1': [5, 4, 0, 0, 3],
    'User2': [4, 0, 0, 2, 4],
    'User3': [0, 0, 5, 3, 0],
    'User4': [0, 2, 4, 0, 0],
    'User5': [1, 0, 0, 5, 4]
}
items = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5']
ratings_matrix = pd.DataFrame(data, index=items).T

# Function to calculate recommendations
def get_recommendations(user, ratings, n_recommendations=2):
    # Compute cosine similarity matrix
    user_similarity = cosine_similarity(ratings.fillna(0))
    sim_df = pd.DataFrame(user_similarity, index=ratings.index, columns=ratings.index)

    # Get the user's similar users
    similar_users = sim_df[user].sort_values(ascending=False)

    # Get the items rated by similar users
    recommendations = pd.Series(dtype=float)

    for similar_user in similar_users.index[1:]:  # Skip the user themselves
        user_ratings = ratings.loc[similar_user]
        if recommendations.empty:
            recommendations = user_ratings[user_ratings > 0]
        else:
            recommendations = pd.concat([recommendations, user_ratings[user_ratings > 0]])

    # Remove items already rated by the user
    recommendations = recommendations[~recommendations.index.isin(ratings.loc[user][ratings.loc[user] > 0].index)]

    # Return the top n recommendations
    return recommendations.sort_values(ascending=False).head(n_recommendations)

# Example usage
user_to_recommend = 'User1'
recommended_items = get_recommendations(user_to_recommend, ratings_matrix)
print(recommended_items)