import pickle
import joblib
import pandas as pd
from sklearn.neighbors import NearestNeighbors

ratings = pd.read_csv(
    '/home/ivs/Documents/MyProjects/SDR/sdr-taller-1/api/data/preprocessed_user_item_rating.csv')
agg_ratings = ratings.groupby('artist-name').agg(mean_rating=('rating', 'mean'),
                                                 number_of_ratings=('rating', 'count')).reset_index().sort_values('number_of_ratings',  ascending=False)
agg_ratings = agg_ratings[agg_ratings['number_of_ratings'] > 10]
ratings_final = pd.merge(
    ratings, agg_ratings[['artist-name']], on='artist-name', how='inner')

print("LLEGO1")
matrix = ratings_final.pivot_table(
    index='artist-name', columns='userid', values='rating')

matrix.to_csv('item-item-matrix.csv', header=True)
df = matrix.copy().fillna(0)

knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(df.values)

pickle.dump(knn, open('item-item-knn.pkl', 'wb'))
pickled_model = pickle.load(open('item-item-knn.pkl', 'rb'))
print(pickled_model)
