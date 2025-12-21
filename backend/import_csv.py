import csv
import sqlite3
import os

# Path to the CSV file
CSV_PATH = '../dataset/cleaned_students.csv'
DB_PATH = 'students.db'

def import_csv_to_db():
    if not os.path.exists(CSV_PATH):
        print(f"CSV file not found: {CSV_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    with open(CSV_PATH, 'r') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            # Map CSV fields to DB fields
            name = f"Student {i}"  # Placeholder name since CSV doesn't have names
            age = int(float(row['age']))
            gender = 'Female' if row['sex'] == 'F' else 'Male'
            study_time = int(row['studytime'])
            past_scores = f"{row['G1']},{row['G2']},{row['G3']}"
            g3 = float(row['G3'])
            if g3 >= 15:
                learning_level = 'high'
            elif g3 >= 10:
                learning_level = 'medium'
            else:
                learning_level = 'low'

            # Insert into DB
            c.execute('INSERT INTO students (name, age, gender, study_time, past_scores, learning_level) VALUES (?, ?, ?, ?, ?, ?)',
                      (name, age, gender, study_time, past_scores, learning_level))

    conn.commit()
    conn.close()
    print("CSV data imported successfully.")

if __name__ == '__main__':
    import_csv_to_db()