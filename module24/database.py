import sqlite3

connection = sqlite3.connect('example.db') #db name

# Create a cursor object to interact with the database
cursor = connection.cursor()

#Create a table named 'employees'
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    departament TEXT NOT NULL,
    salary REAL
    )
''')

connection.commit()

#Insert a new employee
cursor.execute('''
INSERT INTO employees (name, position, departament, salary) 
VALUES(?, ?, ?, ?)
''', ('John Doe', 'Software Engineer', 'IT', '2000'))

connection.commit()

cursor.execute('SELECT * FROM employees')

rows = cursor.fetchall()

for row in rows:
    print(row)

#Update employees
cursor.execute('''
UPDATE employees
SET salary = ?,
WHERE name = ?
''', (3000, 'John Doe'))

connection.commit()

#Delete Employees
cursor.execute('''
DELETE FROM employees
WHERE name = ?
''', ('John Doe'))

connection.commit()

cursor.close()
connection.close()