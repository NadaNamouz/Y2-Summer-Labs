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
    "databaseURL": ""
}

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = '123456'
firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()


@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['pass']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = user
            session['quotes'] = []
            return redirect(url_for('home'))
        except:
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
    except:
    	return render_template('error.html')
  return render_template('signin.html')

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    session['user']=None
    auth.current_user = None
    print("signed out user")
    return redirect(url_for('signin'))

@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        quote = request.form['quote']
        quotes = session['quotes']
        quotes.append(quote)
        session['quotes'] = quotes
        return redirect(url_for('thanks'))
    return render_template('home.html')

@app.route('/thanks', methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')

@app.route('/display', methods=['GET', 'POST'])
def display():
  quote = session['quotes']
  return render_template('display.html', quotes=quote)

@app.route('/error', methods=['GET','POST'])
def error():
	return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
