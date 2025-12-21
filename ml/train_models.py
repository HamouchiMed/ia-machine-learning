import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

# Load the Kaggle Student Performance dataset
data = pd.read_csv('../dataset/cleaned_students.csv')

# Encode categorical columns
le = LabelEncoder()
categorical_cols = ['school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob', 'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic']
for col in categorical_cols:
    data[col] = le.fit_transform(data[col])

# Features for regression (predicting G3 - final grade)
features = ['age', 'studytime', 'failures', 'absences', 'G1', 'G2']
X = data[features]
y = data['G3']

# Drop rows with NaN in target or features
data.dropna(subset=features + ['G3'], inplace=True)
X = data[features]
y = data['G3']

# Split data for training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression for score prediction
lr = LinearRegression()
lr.fit(X_train, y_train)
joblib.dump(lr, 'linear_regression.pkl')

# Decision Tree for level classification (based on G3: low <10, medium 10-15, high >15)
data['level'] = pd.cut(data['G3'], bins=[-1, 10, 15, 21], labels=['Beginner', 'Intermediate', 'Advanced'])
y_level = data['level']
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_level.iloc[X_train.index])
joblib.dump(dt, 'decision_tree.pkl')

# K-Means for clustering students
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_scaled)
joblib.dump(kmeans, 'kmeans.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Models trained and saved using Kaggle Student Performance dataset.")
print(f"Dataset shape: {data.shape}")
print(f"Features used: {features}")
print("Linear Regression R² score on test set:", lr.score(X_test, y_test))