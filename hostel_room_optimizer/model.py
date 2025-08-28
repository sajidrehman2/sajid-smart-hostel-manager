
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import math

def preprocess(df):
    # columns expected: sleep_time, study_pref, cleanliness, smoker, noise_tolerance, region
    numeric_features = ['sleep_time','study_pref','cleanliness','smoker','noise_tolerance']
    categorical_features = ['region']
    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])
    X = preprocessor.fit_transform(df[numeric_features + categorical_features])
    return X, preprocessor

def fit_kmeans(df, n_clusters):
    X, pre = preprocess(df)
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    df2 = df.copy()
    df2['cluster'] = labels
    return df2, km, pre

def allocate_rooms(df, room_capacity=2):
    # Determine number of rooms: ceiling of students/room_capacity
    n_students = len(df)
    n_rooms = math.ceil(n_students / room_capacity)
    # We'll cluster into n_rooms clusters and then pack
    clustered, km, pre = fit_kmeans(df, n_clusters=n_rooms)
    # Group by cluster and distribute into rooms, filling up to room_capacity
    rooms = []
    room_id = 1
    for cluster_label, group in clustered.groupby('cluster'):
        students = group.to_dict('records')
        i = 0
        while i < len(students):
            room_members = students[i:i+room_capacity]
            rooms.append({
                'room_id': room_id,
                'members': [m['name'] for m in room_members],
                'cluster': int(cluster_label)
            })
            room_id += 1
            i += room_capacity
    # If rooms less than n_rooms (rare), create empty rooms
    while len(rooms) < n_rooms:
        rooms.append({'room_id': len(rooms)+1, 'members': [], 'cluster': None})
    return rooms

if __name__ == '__main__':
    df = pd.read_csv('sample_data.csv')
    rooms = allocate_rooms(df, room_capacity=3)
    for r in rooms[:10]:
        print(r)
