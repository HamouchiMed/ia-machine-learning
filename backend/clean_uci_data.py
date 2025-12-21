import pandas as pd

# 1. Load the data
df = pd.read_csv('dirty_students.csv')

# 2. Fix Case Inconsistency (sex column)
df['sex'] = df['sex'].str.upper()

# 3. Handle Missing Values
# If age is missing, use the average. If G3 is missing, assume 0.
df['age'] = df['age'].fillna(df['age'].median())
df['G3'] = df['G3'].fillna(0)

# 4. Remove Duplicates
df = df.drop_duplicates()

# 5. Handle Outliers
# Absences shouldn't be 999. Let's cap them at 100.
df.loc[df['absences'] > 100, 'absences'] = 100

# 6. Save Cleaned Version
df.to_csv('cleaned_students.csv', index=False)
print("Data cleaned and saved to cleaned_students.csv!")