Collaborative Algorithm
    Collaborative Userbased Algorithm
    Collaborative Itembased Algorithm

Required imports when using the collobarative algrithm

    import pandas
    from sklearn.metrics.pairwise import cosine_similarity

This is an example used of the collaboratie Algorithm

    if __name__ == "__main__":
        # Sample user-item rating matrix
        data = {
            'User1': [5, 4, 0, 0, 3],
            'User2': [4, 0, 0, 2, 4],
            'User3': [0, 0, 5, 3, 0],
            'User4': [0, 2, 4, 0, 0],
            'User5': [1, 0, 0, 5, 4]
        }
        items = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5']
        
        # Instantiate recommender system
        recommender = CollaborativeRecommender(data)
        
        # Get recommendations for User1
        user_to_recommend = 'User1'
        recommended_items = recommender.Collaborative(user_to_recommend)
        print(f"Recommended items for {user_to_recommend}:")
        print(recommended_items)
