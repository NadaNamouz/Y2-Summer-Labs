from flask import Flask, render_template, redirect, request, session, url_for
import pyrebase
import logging

Config = {
    "apiKey": "AIzaSyDFbOTe5AAvI00-l1gKh9kQz2LfTuZZwbo",
    "authDomain": "auth--lab.firebaseapp.com",
    "projectId": "auth--lab",
    "storageBucket": "auth--lab.appspot.com",
    "messagingSenderId": "466779299858",
    "appId": "1:466779299858:web:b8a6ee8a3f59101910b8cb",
    "databaseURL": "https://auth--lab-default-rtdb.europe-west1.firebasedatabase.app/"
}

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = '123456'

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['pass']
        name = request.form['fullName']
        username = request.form['username']
        info = {"fullName": name, "email": email, "username": username}
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = user
            session['quotes'] = []
            uid = user['localId']
            db.child("users").child(uid).set(info)
            return redirect(url_for('home'))
        except Exception as e:
            logging.error(f"Error during signup: {e}")
            return render_template('error.html')
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['pass']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            session['quotes'] = []
            return redirect(url_for('home'))
        except Exception as e:
            logging.error(f"Error during signin: {e}")
            return render_template('error.html')
    return render_template('signin.html')

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    session.pop('user', None)
    logging.info("User signed out")
    return redirect(url_for('signin'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        return redirect(url_for('signin'))
    
    if request.method == 'POST':
        try:
            text = request.form['quote']
            name = request.form['person']
            uid = session['user']['localId']
            quote = {"text": text, "said_by": name}
            db.child("users").child(uid).child("quotes").push(quote)
            session['quotes'].append(quote)
            return redirect(url_for('thanks'))
        except Exception as e:
            logging.error(f"Error during quote submission: {e}")
            return render_template('error.html')
    return render_template('home.html')

@app.route('/thanks', methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')

@app.route('/display', methods=['GET', 'POST'])
def display():
    if 'user' not in session:
        return redirect(url_for('signin'))
    
    try:
        uid = session['user']['localId']
        user_data = db.child("users").child(uid).get().val()
        quotes = db.child("users").child(uid).child("quotes").get().val()
        if quotes:
            user_data['quotes'] = quotes.values()
        else:
            user_data['quotes'] = []
        return render_template('display.html', user=user_data)
    except Exception as e:
        logging.error(f"Error during display: {e}")
        return render_template('error.html')

@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
