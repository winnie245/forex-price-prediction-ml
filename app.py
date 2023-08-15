
import numpy as np
from flask import Flask, request, render_template, redirect, session, jsonify
import pickle
from datetime import datetime
 

app = Flask(__name__)

# Load the trained model
with open('linear_regression_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

#define the 'users' dictionary
users = {}  

app.secret_key = 'mkanyama'  #  a secret key for session encryption

@app.route('/')
def home():
    if not session.get('logged_in'):
        # Redirect to the login page if the user is not logged in
        return redirect('/login')
    else:
        # Render the 'index.html' template with the navigation links
        return render_template("index.html", logged_in=session['logged_in'])


@app.route('/login', methods=["GET", "POST"])
def login():
    # Initialize the error message variable
    error_message = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            # Authentication successful
            return redirect('/index')  # Redirect to the index page
        else:
            # Authentication failed
            error_message = 'Invalid username or password'
    return render_template('login.html', error_message=error_message)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        # Validate the input and create a new user account
        if username and password:
            users[username] = password
            return redirect('/login')  # Redirect to the login page after successful sign-up
    
    return render_template("signup.html")


@app.route('/index')
def index():
    # Only authenticated users can access the index page (dashboard)
    # You may add authentication logic here if needed.
    return render_template("index.html")


@app.route('/logout')
def logout():
    # Remove the 'logged_in' session variable when logging out
    session.pop('logged_in', None)
    # Redirect to the login page after logging out
    return redirect('/login')

@app.route("/getting_prediction", methods=["POST"])
def getprediction():
   date_string = request.form["Date"]
        date = datetime.strptime(date_string, '%Y-%m-%d')
        input = np.array([date.day]) 
        final_input = np.array(input).reshape(1, -1)
        # Process form data and make prediction
        close = float(request.form['close'])
        inflation_rate = float(request.form['inflation_rate'])
        unemployment_rate = float(request.form['unemployment_rate'])
        prediction = model.predict([[close, inflation_rate, unemployment_rate]])
        return render_template('index.html', output='Predicted forex price: {}'.format(prediction[0]))
if __name__ == "__main__":
    app.run(debug=True)
