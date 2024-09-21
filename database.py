import sqlite3

DATABASE = 'database.db'

def connect_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

def init_db():
    """Initialize the database with necessary tables."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            shift_time TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    
    conn.commit()
    conn.close()
    
def insert_user(name, email, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
              (name, email, password))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def insert_employee(name, position):
    """Insert a new employee into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name, position) VALUES (?, ?)", (name, position))
    conn.commit()
    conn.close()

def get_employees():
    """Get all employees from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return employees

def insert_shift(employee_id, shift_time):
    """Insert a new shift into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO shifts (employee_id, shift_time) VALUES (?, ?)", (employee_id, shift_time))
    conn.commit()
    conn.close()

def get_shifts():
    """Get all shifts from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shifts")
    shifts = cursor.fetchall()
    conn.close()
    return shifts

def insert_attendance(employee_id, date, status):
    """Insert a new attendance record into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (employee_id, date, status) VALUES (?, ?, ?)", (employee_id, date, status))
    conn.commit()
    conn.close()

def get_attendance():
    """Get all attendance records from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    attendance_records = cursor.fetchall()
    conn.close()
    return attendance_records


def insert_task(employee_id, task, status):
    """Insert a new task into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (employee_id, task, status) VALUES (?, ?, ?)", (employee_id, task, status))
    conn.commit()
    conn.close()

def get_tasks():
    """Get all tasks from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_employee(employee_id):
    """Delete an employee from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    conn.commit()
    conn.close()

def delete_shift(shift_id):
    """Delete a shift from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shifts WHERE id = ?", (shift_id,))
    conn.commit()
    conn.close()

def delete_attendance(attendance_id):
    """Delete an attendance record from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance WHERE id = ?", (attendance_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Delete a task from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_shifts_with_names():
    """Get all shifts from the database with employee names."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT shifts.id, employees.name, shifts.shift_time 
        FROM shifts 
        JOIN employees ON shifts.employee_id = employees.id
    """)
    shifts = cursor.fetchall()
    conn.close()
    return shifts

def get_attendance_with_names():
    """Get all attendance records from the database with employee names."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT attendance.id, employees.name, attendance.date, attendance.status 
        FROM attendance 
        JOIN employees ON attendance.employee_id = employees.id
    """)
    attendance_records = cursor.fetchall()
    conn.close()
    return attendance_records

def get_tasks_with_names():
    """Get all tasks from the database with employee names."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tasks.id, employees.name, tasks.task, tasks.status 
        FROM tasks 
        JOIN employees ON tasks.employee_id = employees.id
    """)
    tasks = cursor.fetchall()
    conn.close()
    return tasks