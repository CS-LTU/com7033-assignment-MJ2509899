from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from models.auth_db import init_auth_db, register_user, validate_user
from models.pateint_db import init_patient_db, add_patient, get_all_patients, get_patient, update_patient, delete_patient

app = Flask(__name__)
app.secret_key = 'your_secure_random_secret'
csrf = CSRFProtect(app)

# Initialize databases
init_auth_db()
init_patient_db(app)

# ----------------- Authentication Routes -----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user(username, password)
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_user(username, password):
            session['username'] = username
            flash('Login successful.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

# ----------------- Patient CRUD Routes -----------------

def login_required(f):
    """Decorator to ensure user is logged in"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    patients = get_all_patients()
    return render_template('index.html', patients=patients)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']
        add_patient(name, age, disease)
        flash('Patient added successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('add_patient.html')

@app.route('/edit/<patient_id>', methods=['GET', 'POST'])
@login_required
def edit(patient_id):
    patient = get_patient(patient_id)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']
        update_patient(patient_id, name, age, disease)
        flash('Patient updated successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_patient.html', patient=patient)

@app.route('/delete/<patient_id>')
@login_required
def delete(patient_id):
    delete_patient(patient_id)
    flash('Patient deleted successfully.', 'success')
    return redirect(url_for('index'))

# ----------------- Run App -----------------

if __name__ == '__main__':
    app.run(debug=True)
