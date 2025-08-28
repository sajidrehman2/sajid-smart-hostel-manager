
import pandas as pd
import numpy as np
import random

def generate_student(n=50, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    rows = []
    regions = ['North', 'South', 'East', 'West', 'Central']
    for i in range(n):
        name = f"Student_{i+1:03d}"
        # sleep_time: typical sleep hour (0-23)
        sleep_time = int(np.clip(np.random.normal(1 if np.random.rand()<0.5 else 23, 2) % 24, 0, 23))
        # study_pref: 0 (low) - 10 (high)
        study_pref = int(np.clip(np.random.normal(6, 2), 0, 10))
        # cleanliness: 0-10
        cleanliness = int(np.clip(np.random.normal(6, 2), 0, 10))
        # smoker: 0/1
        smoker = int(np.random.rand() < 0.1)
        # noise_tolerance: 0-10 (higher means tolerates noise)
        noise_tolerance = int(np.clip(np.random.normal(5, 2), 0, 10))
        # hometown region
        region = np.random.choice(regions)
        rows.append({
            'name': name,
            'sleep_time': sleep_time,
            'study_pref': study_pref,
            'cleanliness': cleanliness,
            'smoker': smoker,
            'noise_tolerance': noise_tolerance,
            'region': region
        })
    return pd.DataFrame(rows)

if __name__ == '__main__':
    df = generate_student(60)
    df.to_csv('sample_data.csv', index=False)
    print('Wrote sample_data.csv with', len(df), 'rows')
