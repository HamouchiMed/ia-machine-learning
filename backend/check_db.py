import sqlite3

conn = sqlite3.connect('students.db')
c = conn.cursor()

# Get table names
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in c.fetchall()]
print('Tables:', tables)

# Count records in students
c.execute('SELECT COUNT(*) FROM students')
students_count = c.fetchone()[0]
print('Students count:', students_count)

# Count records in quiz_results
c.execute('SELECT COUNT(*) FROM quiz_results')
quiz_count = c.fetchone()[0]
print('Quiz results count:', quiz_count)

conn.close()