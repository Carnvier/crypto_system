import sqlite3

conn = sqlite3.connect('practice_db.db')

c = conn.cursor()

def create_db():
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            department TEXT NOT NULL
        )
        '''
    )

def insert_data():   
    employees = [
        ('John Doe', 30, 'HR'),
        ('Jane Smith', 25, 'IT'),
        ('Michael Johnson', 35, 'Finance')
    ]

    c.executemany('''
    INSERT INTO Employees (name, age, department)
    VALUES(?, ?, ?)
    ''', employees
    )

def print_employees():
    c.execute("SELECT * FROM Employees")
    employees = c.fetchall()

    print("Products Table Data:")
    print("-"*42)
    print("| id | name           | age | department |")
    print("-"*42)
    for employee in employees:
        print(f"| {employee[0]} | {employee[1]:<15} | {employee[2]}  | {employee[3]:<10} |")
    print("-"*42)

def update_employees():
    c.execute("""
    UPDATE Employees
    SET age = ?
    WHERE id = ?
    """, (21, 2))

    conn.commit()
    print(f'Updated {c.rowcount} record(s)')

def delete_employee():
    c.execute("DELETE FROM Employees WHERE id = ?", (2,))

    conn.commit()
    print(f'Deleted {c.rowcount} record(s)')

c.execute("SELECT * FROM Employees WHERE age > ?", (32,))
employees = c.fetchall()

print("Employees older than 32:")

print("-"*42)

print("| id | name           | age | department |")

print("-"*42)

for employee in employees:
    print(f"| {employee[0]} | {employee[1]:<15} | {employee[2]}  | {employee[3]:<10} |")

print("-"*42)

c.close()
conn.close()

