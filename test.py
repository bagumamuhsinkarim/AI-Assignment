import CollaborativeRecommender

# Sample ratings data
ratings = {
    "User1": [5, 3, 4, 2, 1],
    "User2": [4, 1, 2, 5, 3],
    "User3": [3, 2, 1, 4, 5],
    "User4": [2, 5, 3, 1, 4],
    "User5": [1, 4, 5, 3, 2],
}

# Create a CollaborativeRecommender object
recommender = CollaborativeRecommender.CollaborativeRecommender(ratings)

# Compute similarity matrix
recommender.person_Correlation()

# User-based recommendations
user_recommendations = recommender.CollaborativeUser("User1")
print("User-based recommendations for User1:")
print(user_recommendations)

# Item-based recommendations
item_recommendations = recommender.CollaborativeItem(3)
print("Item-based recommendations for item 3:")
print(item_recommendations)

# Hybrid recommendations
hybrid_recommendations = recommender.CollaborativeHybrid("User1", 3)
print("Hybrid recommendations for User1 and item 3:")
print(hybrid_recommendations)