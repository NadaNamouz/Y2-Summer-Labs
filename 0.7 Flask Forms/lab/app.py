from flask import Flask, render_template,url_for,redirect,request
import random

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        month = request.form['BM']
       
        return redirect(url_for('fortune',
            birthmonth = month))

@app.route("/fortune",methods=['GET', 'POST'])
def fortune():
    if request.method == 'POST':
        month = request.form['BM']
    fortunes = ["you will become rich this year",
        "An unexpected event will bring you joy soon",
        "You will achieve your goals",
        "A pleasant surprise is waiting for you",
        "Good news is coming your way",
        "You will have a great day today",
        "Success will be yours",
        "Happiness is in your future",
        "Expect good news soon",
        "You will make a new friend",
        "An adventure is in store for you"]
    x = len(month)
    if x>10:
        f = "hello"
    elif x==0:
        return render_template("home.html")

    else:
        f = fortunes[x]
        return render_template("fortune.html",f=f)




if __name__ == '__main__':
    app.run(debug=True)

