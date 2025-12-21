from flask import Flask, request, jsonify
from flask_cors import CORS
import db
import joblib
import numpy as np
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load ML models
lr = joblib.load('../ml/linear_regression.pkl')
dt = joblib.load('../ml/decision_tree.pkl')
kmeans = joblib.load('../ml/kmeans.pkl')
scaler = joblib.load('../ml/scaler.pkl')

# Sample quiz questions
questions = {
    'easy': [
        {'question': 'What is 2+2?', 'options': ['3', '4', '5', '6'], 'answer': '4'},
        {'question': 'What is 5*3?', 'options': ['15', '16', '17', '18'], 'answer': '15'}
    ],
    'medium': [
        {'question': 'What is 12/3?', 'options': ['3', '4', '5', '6'], 'answer': '4'},
        {'question': 'What is 7*8?', 'options': ['54', '56', '58', '60'], 'answer': '56'}
    ],
    'hard': [
        {'question': 'What is 15*13?', 'options': ['195', '196', '197', '198'], 'answer': '195'},
        {'question': 'What is 144/12?', 'options': ['11', '12', '13', '14'], 'answer': '12'}
    ]
}

@app.route('/student', methods=['POST'])
def add_student():
    data = request.json
    student_id = db.add_student(data['name'], data['age'], data['gender'], data['study_time'], data['past_scores'], data['learning_level'])
    return jsonify({'student_id': student_id})

@app.route('/students', methods=['GET'])
def get_students():
    students = db.get_students()
    return jsonify(students)

@app.route('/quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    db.add_quiz_result(data['student_id'], data['subject'], data['score'], data['difficulty'], datetime.now().isoformat())
    return jsonify({'message': 'Quiz result saved'})

@app.route('/performance/<int:student_id>', methods=['GET'])
def get_performance(student_id):
    results = db.get_quiz_results(student_id)
    return jsonify(results)

@app.route('/predict', methods=['POST'])
def predict_score():
    data = request.json
    # Map frontend data to model features: [age, studytime, failures, absences, G1, G2]
    # Using defaults for missing data
    features = [
        16,  # default age
        data.get('studytime', 2),
        0,   # default failures
        data.get('absences', 0),
        data.get('past_grade', 10),  # G1
        data.get('past_grade', 10)   # G2
    ]
    pred = lr.predict([features])[0]
    return jsonify({'predicted_score': round(float(pred), 2)})

@app.route('/classify', methods=['POST'])
def classify_level():
    data = request.json
    features = [
        16,  # default age
        data.get('studytime', 2),
        0,   # default failures
        data.get('absences', 0),
        data.get('past_grade', 10),  # G1
        data.get('past_grade', 10)   # G2
    ]
    level = dt.predict([features])[0]
    return jsonify({'level': level})

@app.route('/cluster', methods=['POST'])
def cluster_student():
    data = request.json
    features = [
        16,  # default age
        data.get('studytime', 2),
        0,   # default failures
        data.get('absences', 0),
        data.get('past_grade', 10),  # G1
        data.get('past_grade', 10)   # G2
    ]
    scaled = scaler.transform([features])
    cluster = int(kmeans.predict(scaled)[0])
    return jsonify({'cluster': cluster})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    features = [
        16,  # default age
        data.get('studytime', 2),
        0,   # default failures
        data.get('absences', 0),
        data.get('past_grade', 10),  # G1
        data.get('past_grade', 10)   # G2
    ]
    scaled = scaler.transform([features])
    cluster = kmeans.predict(scaled)[0]
    # Simple recommendations based on cluster
    recs = {
        0: 'Increase study time',
        1: 'Focus on weak subjects',
        2: 'Practice more quizzes'
    }
    return jsonify({'recommendation': recs.get(cluster, 'General improvement')})

@app.route('/quiz/<difficulty>', methods=['GET'])
def get_quiz(difficulty):
    if difficulty not in questions:
        return jsonify({'error': 'Invalid difficulty'}), 400
    return jsonify(questions[difficulty])

if __name__ == '__main__':
    db.init_db()
    app.run(host='0.0.0.0', debug=True)