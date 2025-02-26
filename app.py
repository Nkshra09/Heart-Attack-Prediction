# app.py
from flask import Flask, redirect, request, render_template,url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash

import pickle
# from joblib import load
import numpy as np


app = Flask(__name__)
app.secret_key = 'your_secret_key'

users={}
@app.route('/some_existing_route')
def some_existing_route():
    return "This is an existing route."

# Load the model using pickle
with open('Heartmodel.pkl', 'rb') as model_file:
     model = pickle.load(model_file)

# model = load('model.joblib')
@app.route('/')
def input():
    return render_template('index.html')

@app.route('/input')
def home():
    return render_template('input.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/doctors')
def doctors():
    return render_template('blog-single.html')


users={}
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    # Check if the user exists and the password matches
    if email in users and users[email] == password:
        flash('Login successful!', 'success')
    else:
        flash('Invalid email or password', 'danger')
    return redirect(url_for('register'))

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    # Check if the user already exists
    if email in users:
        flash('Email already registered. Please login.', 'danger')
    elif password != confirm_password:
        flash('Passwords do not match.', 'danger')
    else:
        # Register the new user
        users[email] = password
        flash('Signup successful!', 'success')
    return redirect(url_for('register'))



@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features from form inputs
        age = int(request.form['age'])
        sex = int(request.form['sex'])
        cp = int(request.form['cp'])
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        fbs = int(request.form['fbs'])
        restecg = int(request.form['restecg'])
        thalach = int(request.form['thalach'])
        exang = int(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        slope = int(request.form['slope'])
        ca = int(request.form['ca'])
        thal = int(request.form['thal'])

        # Combine features into a single array
        features = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

        # Make prediction
        prediction = model.predict(features)

        # Determine the prediction result
        output = 'Yes' if prediction[0] == 1 else 'No'
        if prediction[0] == 1:
                prediction_text = (
            "The patient is predicted to have a heart attack. "
            # "It is highly recommended to seek immediate medical attention. "
            # "Preventative measures such as lifestyle changes, medications, and regular medical checkups are crucial. "
            # "Consult with a healthcare provider for a detailed action plan."
        )
                consult_doctor = True
        else:
                prediction_text = (
            "The patient is predicted not to have a heart attack. "
            # "While this is a positive outcome, it's important to continue maintaining a healthy lifestyle. "
            # "Regular exercise, a balanced diet, and routine health checkups can help prevent future health issues. "
            "Stay proactive about your heart health and consult with a healthcare provider for personalized advice."
        )
                consult_doctor = False
        return render_template('result.html', prediction_text=prediction_text,consult_doctor=consult_doctor)

        
    
    except ValueError as e:
        # Handle invalid input
        return render_template('result.html', prediction_text=f'Error: {str(e)}. Please check your inputs and try again.')

    except Exception as e:
        # Handle other exceptions
        return render_template('result.html', prediction_text=f'An error occurred: {str(e)}. Please try again later.')

if __name__ == "__main__":
    app.run(debug=True)



