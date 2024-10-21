class RecommenderSystem:
    def __init__(self, ratings_data):
        self.ratings = pandas.DataFrame(ratings_data).T
        self.similarity_matrix = None
    
    def calculate_similarity(self):
        self.similarity_matrix = cosine_similarity(self.ratings.fillna(0))
        self.similarity_matrix = pandas.DataFrame(self.similarity_matrix,index=self.ratings.index,columns=self.ratings.index)
    
    def get_recommendations(self, user, n_recommendations=2):        
        if self.similarity_matrix is None:
            self.calculate_similarity()

        # Get similar users
        similar_users = self.similarity_matrix[user].sort_values(ascending=False)

        # Gather items from similar users
        recommendations = pandas.Series(dtype=float)
        for similar_user in similar_users.index[1:]:  # Skip the user themselves
            user_ratings = self.ratings.loc[similar_user]
            recommendations = pandas.concat([recommendations, user_ratings[user_ratings > 0]])

        # Remove items already rated by the user
        recommendations = recommendations[~recommendations.index.isin(
            self.ratings.loc[user][self.ratings.loc[user] > 0].index)]

        return recommendations.sort_values(ascending=False).head(n_recommendations)