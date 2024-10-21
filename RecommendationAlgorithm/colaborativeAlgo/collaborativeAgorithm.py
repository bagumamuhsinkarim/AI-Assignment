class CollaborativeRecommender:
    def __init__(self, ratings_data):       #initializes an instance of the class with ratings_data
        self.ratings = pandas.DataFrame(ratings_data).T
        self.similarity_matrix = None       #will be computed later based on ratings.
    
    def calculate_similarity(self):     #likely between users or items in the dataset based on their ratings.
        self.similarity_matrix = cosine_similarity(self.ratings.fillna(0))      #reeplace any missing values with 0 or null values.
        self.similarity_matrix = pandas.DataFrame(self.similarity_matrix,index=self.ratings.index,columns=self.ratings.index)
        
        """
            similariy_df = pandas.DataFrame(self.similarity_matrix)    #Dataframe creation
            similarity_df.index = self.ratings.index
            similarity_df.columns = self.ratings.index
            self.similarity_matrix = similarity_df
        """

    def Collaborative(self, user, n_recommendations=2):        
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