import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# Load the user's custom dataset
df = pd.read_csv('dataset/student_performance.csv')

# Select features for models
features = ['age', 'studytime', 'failures', 'absences', 'G1', 'G2']
target_regression = 'G3'

# Prepare data for regression (predict G3)
X_reg = df[features]
y_reg = df[target_regression]

# Split data
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

# Train Linear Regression
lr = LinearRegression()
lr.fit(X_train_reg, y_train_reg)

# For classification, let's classify based on G3 ranges (e.g., low, medium, high)
def classify_grade(g3):
    if g3 < 10:
        return 'low'
    elif g3 < 15:
        return 'medium'
    else:
        return 'high'

df['grade_level'] = df['G3'].apply(classify_grade)
y_class = df['grade_level']

# Split for classification
X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(X_reg, y_class, test_size=0.2, random_state=42)

# Train Decision Tree Classifier
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train_class, y_train_class)

# For clustering, use all features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_reg)

# Train KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_scaled)

# Save models
joblib.dump(lr, './ml/linear_regression.pkl')
joblib.dump(dt, './ml/decision_tree.pkl')
joblib.dump(kmeans, './ml/kmeans.pkl')
joblib.dump(scaler, './ml/scaler.pkl')

print("Models retrained and saved using your custom student performance dataset!")