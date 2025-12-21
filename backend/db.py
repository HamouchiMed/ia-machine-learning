import sqlite3
import os

DB_PATH = 'students.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        study_time REAL,
        past_scores TEXT,
        learning_level TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        subject TEXT,
        score REAL,
        difficulty TEXT,
        date TEXT,
        FOREIGN KEY (student_id) REFERENCES students (id)
    )''')
    conn.commit()
    conn.close()

def add_student(name, age, gender, study_time, past_scores, learning_level):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO students (name, age, gender, study_time, past_scores, learning_level) VALUES (?, ?, ?, ?, ?, ?)',
              (name, age, gender, study_time, past_scores, learning_level))
    student_id = c.lastrowid
    conn.commit()
    conn.close()
    return student_id

def get_students():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()
    return students

def add_quiz_result(student_id, subject, score, difficulty, date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO quiz_results (student_id, subject, score, difficulty, date) VALUES (?, ?, ?, ?, ?)',
              (student_id, subject, score, difficulty, date))
    conn.commit()
    conn.close()

def get_quiz_results(student_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM quiz_results WHERE student_id = ?', (student_id,))
    results = c.fetchall()
    conn.close()
    return results

def get_student(student_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = c.fetchone()
    conn.close()
    return student