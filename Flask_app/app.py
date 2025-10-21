from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    disease = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Patient {self.name}>"

# Initialize database
with app.app_context():
    db.create_all()

# Home page: List all patients
@app.route('/')
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

# Add a new patient
@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']
        new_patient = Patient(name=name, age=age, disease=disease)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_patient.html')

# Edit patient
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.disease = request.form['disease']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_patient.html', patient=patient)

# Delete patient
@app.route('/delete/<int:id>', methods=['GET'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
