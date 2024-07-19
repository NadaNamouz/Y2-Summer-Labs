from flask import Flask, render_template, redirect, request, session, url_for

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = "123456"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        n = request.form['name']
        b = request.form['month']
        session['name'] = n
        session['BirthMonth'] = b
        return redirect(url_for('homepage'))
    return render_template('home.html')

@app.route("/fortune", methods=['GET'])
def fortune():
    fortunes = [
        "you will become rich this year",
        "An unexpected event will bring you joy soon",
        "You will achieve your goals",
        "A pleasant surprise is waiting for you",
        "Good news is coming your way",
        "You will have a great day today",
        "Success will be yours",
        "Happiness is in your future",
        "Expect good news soon",
        "You will make a new friend",
        "An adventure is in store for you"
    ]
    month = session.get('BirthMonth', '')
    x = len(month)
    if x > 10 or x == 0:
        return redirect(url_for('login'))
    f = fortunes[x]
    return render_template("fortune.html", f=f)

if __name__ == '__main__':
    app.run(debug=True)
