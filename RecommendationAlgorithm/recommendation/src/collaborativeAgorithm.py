import pandas
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeRecommender:
    def __init__(self, ratings_data):       #initializes an instance of the class with ratings_data
        #error handling to ensure the input data is valid.
        if not isinstance(ratings_data, dict):
            raise ValueError("ratings data should be a dictionary")

        # Check if all keys are strings and all values are lists
        for key, value in ratings_data.items():
            if not isinstance(key, str) or not isinstance(value, list):
                raise ValueError("All keys should be strings and all values should be lists")
            
            if not all(isinstance(x, (int, float)) or pandas.isna(x) for x in value):
                raise ValueError("All values in lists should be numeric or NaN.")

        self.ratings = pandas.DataFrame(ratings_data).T
        self.similarity_matrix = None       #will be computed later based on ratings.
    
    def person_Correlation(self):     #likely between users or items in the dataset based on their ratings.
        self.similarity_matrix = cosine_similarity(self.ratings.fillna(0))      #replace any missing values with 0 or null values.
        self.similarity_matrix = pandas.DataFrame(self.similarity_matrix,index=self.ratings.index,columns=self.ratings.index)
        
        """
            similariy_df = pandas.DataFrame(self.similarity_matrix)    #Dataframe creation
            similarity_df.index = self.ratings.index
            similarity_df.columns = self.ratings.index
            self.similarity_matrix = similarity_df
        """

    def CollaborativeUser(self, user, Required_Recommendations=3):        
        if self.similarity_matrix is None:
            self.person_Correlation()

        # Get and sort similar users
        similar_users = self.similarity_matrix[user].sort_values(ascending=False)

        # Gather items from similar users
        recommendations = pandas.Series(dtype=float)

        for similar_user in similar_users.index[1:]:  # Skip the user themselves
            user_ratings = self.ratings.loc[similar_user]
            recommendations = pandas.concat([recommendations, user_ratings[user_ratings > 0]])

        # Remove items already rated by the same user
        recommendations = recommendations[~recommendations.index.isin(
            self.ratings.loc[user][self.ratings.loc[user] > 0].index)]

        return recommendations.sort_values(ascending=False).head(Required_Recommendations)
    
    def CollaborativeItem(self, item, Required_Recommendations=3):
        if self.similarity_matrix is None:
            self.person_Correlation()

        # Get and sort similar items
        similar_items = self.similarity_matrix[item].sort_values(ascending=False)

        # Gather items from similar items
        recommendations = pandas.Series(dtype=float)
        for similar_item in similar_items.index[1:]:
            if similar_item in self.ratings:
                item_ratings = self.ratings[similar_item]
                recommendations = pandas.concat([recommendations, item_ratings[item_ratings > 0]])
            else:
                return f"Warning: {similar_item} not found in ratings"

        # Remove items already rated by the same user
        recommendations = recommendations[~recommendations.index.isin(
            self.ratings[item][self.ratings[item] > 0].index)]
        
        return recommendations.sort_values(ascending=False).head(Required_Recommendations)
       
    def CollaborativeHybrid(self, user, item, Required_Recommendations=3):
        if self.similarity_matrix is None:
            self.person_Correlation()

        # Get and sort similar users
        similar_users = self.similarity_matrix[user].sort_values(ascending=False)

        # Gather items from similar users
        recommendations = pandas.Series(dtype=float)
        for similar_user in similar_users.index[1:]:
            user_ratings = self.ratings.loc[similar_user]
            recommendations = pandas.concat([recommendations, user_ratings[user_ratings > 0]])

        # Remove items already rated by the same user
        recommendations = recommendations[~recommendations.index.isin(
            self.ratings.loc[user][self.ratings.loc[user] > 0].index)]
        
        # Get and sort similar items
        similar_items = self.similarity_matrix[item].sort_values(ascending=False)

        # Gather items from similar items
        recommendations2 = pandas.Series(dtype=float)
        for similar_item in similar_items.index[1:]:
            item_ratings = self.ratings[similar_item]
            recommendations2 = pandas.concat([recommendations2, item_ratings[item_ratings > 0]])

        # Remove items already rated by the same user
        recommendations2 = recommendations2[~recommendations2.index.isin(
            self.ratings[item][self.ratings[item] > 0].index)]
        
        recommendations = recommendations.append(recommendations2)

        return recommendations.sort_values(ascending=False).head(Required_Recommendations)
    