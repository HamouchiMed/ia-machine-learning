import pandas as pd
import numpy as np
import random

num_records = 8000

def generate_dirty_uci():
    data = {
        'school': [random.choice(['GP', 'MS']) for _ in range(num_records)],
        'sex': [random.choice(['F', 'M']) for _ in range(num_records)],
        'age': [random.randint(15, 22) for _ in range(num_records)],
        'address': [random.choice(['U', 'R']) for _ in range(num_records)],
        'famsize': [random.choice(['GT3', 'LE3']) for _ in range(num_records)],
        'Pstatus': [random.choice(['A', 'T']) for _ in range(num_records)],
        'Medu': [random.randint(0, 4) for _ in range(num_records)],
        'Fedu': [random.randint(0, 4) for _ in range(num_records)],
        'Mjob': [random.choice(['at_home', 'health', 'other', 'services', 'teacher']) for _ in range(num_records)],
        'Fjob': [random.choice(['at_home', 'health', 'other', 'services', 'teacher']) for _ in range(num_records)],
        'reason': [random.choice(['course', 'other', 'home', 'reputation']) for _ in range(num_records)],
        'guardian': [random.choice(['mother', 'father', 'other']) for _ in range(num_records)],
        'traveltime': [random.randint(1, 4) for _ in range(num_records)],
        'studytime': [random.randint(1, 4) for _ in range(num_records)],
        'failures': [random.randint(0, 3) for _ in range(num_records)],
        'schoolsup': [random.choice(['yes', 'no']) for _ in range(num_records)],
        'famsup': [random.choice(['yes', 'no']) for _ in range(num_records)],
        'paid': [random.choice(['yes', 'no']) for _ in range(num_records)],
        'activities': [random.choice(['yes', 'no']) for _ in range(num_records)],
        'nursery': [random.choice(['yes', 'no']) for _ in range(num_records)],
        'higher': [random.choice(['yes', 'no']) for _ in range(num_records)],
        'internet': [random.choice(['yes', 'no']) for _ in range(num_records)],
        'romantic': [random.choice(['yes', 'no']) for _ in range(num_records)],
        'famrel': [random.randint(1, 5) for _ in range(num_records)],
        'freetime': [random.randint(1, 5) for _ in range(num_records)],
        'goout': [random.randint(1, 5) for _ in range(num_records)],
        'Dalc': [random.randint(1, 5) for _ in range(num_records)],
        'Walc': [random.randint(1, 5) for _ in range(num_records)],
        'health': [random.randint(1, 5) for _ in range(num_records)],
        'absences': [random.randint(0, 93) for _ in range(num_records)],
        'G1': [random.randint(0, 20) for _ in range(num_records)],
        'G2': [random.randint(0, 20) for _ in range(num_records)],
        'G3': [random.randint(0, 20) for _ in range(num_records)]
    }

    df = pd.DataFrame(data)

    # --- INJECT DIRT ---
    # 1. Duplicates
    df = pd.concat([df, df.iloc[:100]], ignore_index=True)
    # 2. Missing Values (NaN)
    for _ in range(300):
        df.loc[random.randint(0, 8099), 'age'] = np.nan
        df.loc[random.randint(0, 8099), 'G3'] = np.nan
    # 3. Typos
    df.loc[0:20, 'sex'] = 'f'  # Lowercase instead of 'F'
    # 4. Outliers
    df.loc[50:60, 'absences'] = 999 

    df.to_csv('dirty_students.csv', index=False)
    print("Dirty dataset created: dirty_students.csv")

generate_dirty_uci()