from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import init_db, insert_employee, get_employees, insert_shift, get_shifts_with_names
from database import insert_attendance, get_attendance_with_names, insert_task, get_tasks_with_names
from database import delete_employee, delete_shift, delete_attendance, delete_task
from database import insert_user, get_user_by_email
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_statistics():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Count number of employees
    cursor.execute("SELECT COUNT(*) FROM employees")
    no_of_employees = cursor.fetchone()[0]

    # Count number of tasks
    cursor.execute("SELECT COUNT(*) FROM tasks")
    no_of_tasks = cursor.fetchone()[0]

    # Count number of shifts
    cursor.execute("SELECT COUNT(*) FROM shifts")
    no_of_shifts = cursor.fetchone()[0]

    # Count number of attendance present
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'Present'")
    no_of_present = cursor.fetchone()[0]

    # Count number of attendance absent
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'Absent'")
    no_of_absent = cursor.fetchone()[0]

    conn.close()

    return no_of_employees, no_of_tasks, no_of_shifts, no_of_present, no_of_absent

@app.route('/performance')
def performance():
    no_of_employees, no_of_tasks, no_of_shifts, no_of_present, no_of_absent = get_statistics()
    return render_template('performance.html', 
                            no_of_employees=no_of_employees,
                            no_of_tasks=no_of_tasks,
                            no_of_shifts=no_of_shifts,
                            no_of_present=no_of_present,
                            no_of_absent=no_of_absent)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = get_user_by_email(email)
        
        if user and check_password_hash(user[3], password):  # Assuming password is the 4th column
            session['user_id'] = user[0]  # Assuming id is the 1st column
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)
        
        try:
            insert_user(name, email, hashed_password)
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists', 'error')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# Add the login_required decorator to all your existing routes
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        insert_employee(name, position)
        return redirect(url_for('employees'))

    employees = get_employees()
    return render_template('employees.html', employees=employees)

@app.route('/delete_employee/<int:employee_id>')
def delete_employee_route(employee_id):
    delete_employee(employee_id)
    return redirect(url_for('employees'))

@app.route('/shifts', methods=['GET', 'POST'])
def shifts():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        shift_time = request.form['shift_time']
        insert_shift(employee_id, shift_time)
        return redirect(url_for('shifts'))

    shifts = get_shifts_with_names()
    employees = get_employees()
    return render_template('shifts.html', shifts=shifts, employees=employees)

@app.route('/delete_shift/<int:shift_id>')
def delete_shift_route(shift_id):
    delete_shift(shift_id)
    return redirect(url_for('shifts'))

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        date = request.form['date']
        status = request.form['status']
        insert_attendance(employee_id, date, status)
        return redirect(url_for('attendance'))

    attendance_records = get_attendance_with_names()
    employees = get_employees()
    return render_template('attendance.html', attendance_records=attendance_records, employees=employees)

@app.route('/delete_attendance/<int:attendance_id>')
def delete_attendance_route(attendance_id):
    delete_attendance(attendance_id)
    return redirect(url_for('attendance'))

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        task = request.form['task']
        status = request.form['status']
        insert_task(employee_id, task, status)
        return redirect(url_for('tasks'))

    tasks = get_tasks_with_names()
    employees = get_employees()
    return render_template('tasks.html', tasks=tasks, employees=employees)

@app.route('/delete_task/<int:task_id>')
def delete_task_route(task_id):
    delete_task(task_id)
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)