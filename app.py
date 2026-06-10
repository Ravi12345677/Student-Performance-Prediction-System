from flask import Flask,render_template,request,redirect,session
import sqlite3
import pickle
import numpy as np


def create_table():
    conn = sqlite3.connect('database.db')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    ''')

    conn.commit()
    conn.close()

create_table()

app = Flask(__name__)
app.secret_key="studentproject"

model = pickle.load(
    open("models/student_model.pkl", "rb")
)


@app.route('/')
def home():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        session['user'] = user[1]
        return redirect('/dashboard')

    return "Invalid Email or Password"

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():

    if request.method == 'POST':

        name = request.form['name']

        attendance = float(request.form['attendance'])
        study_hours = float(request.form['study_hours'])
        assignment = float(request.form['assignment'])
        previous = float(request.form['previous'])

        prediction = model.predict([
            [
                attendance,
                study_hours,
                assignment,
                previous
            ]
        ])

        result = round(prediction[0], 2)

        # Keep result within 0-100
        if result > 100:
            result = 100

        if result < 0:
            result = 0

        # Performance Status
        if result >= 80:
            status = "Excellent"
        elif result >= 60:
            status = "Good"
        else:
            status = "Needs Improvement"

        # Grade Calculation
        if result >= 90:
            grade = "A+"
        elif result >= 80:
            grade = "A"
        elif result >= 70:
            grade = "B"
        elif result >= 60:
            grade = "C"
        elif result >= 50:
            grade = "D"
        else:
            grade = "F"

        session['name'] = name

        session['attendance'] = attendance
        session['study_hours'] = study_hours
        session['assignment'] = assignment
        session['previous'] = previous
        session['prediction'] = result

        session['grade'] = grade
        session['status'] = status

        

        return render_template(
            'report.html',
            name=name,
            attendance=attendance,
            study_hours=study_hours,
            assignment=assignment,
            previous=previous,
            prediction=result,
            status=status,
            grade=grade
        )

    return render_template('prediction.html')

@app.route('/graph')
def graph():

    return render_template(
        'graph.html',

        name=session.get('name', 'Student'),

        attendance=session.get('attendance', 0),
        study_hours=session.get('study_hours', 0),
        assignment=session.get('assignment', 0),
        previous=session.get('previous', 0),
        prediction=session.get('prediction', 0),

        grade=session.get('grade', 'N/A'),
        status=session.get('status', 'N/A')
    )

@app.route('/report')
def report():

    return render_template(
        'report.html',

        name=session.get('name', 'Student'),

        attendance=session.get('attendance', 0),
        study_hours=session.get('study_hours', 0),
        assignment=session.get('assignment', 0),
        previous=session.get('previous', 0),
        prediction=session.get('prediction', 0),

        grade=session.get('grade', 'N/A'),
        status=session.get('status', 'N/A')
    )

if __name__=="__main__":
    app.run(debug=True)