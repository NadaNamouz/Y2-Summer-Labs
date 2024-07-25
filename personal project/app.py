from flask import Flask, render_template, redirect, request, session, url_for, jsonify
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyCRizJoiuEBn2DZg38MlYDji2fRSVCpXHY",
  "authDomain": "personal-project-final.firebaseapp.com",
  "projectId": "personal-project-final",
  "storageBucket": "personal-project-final.appspot.com",
  "messagingSenderId": "46796258106",
  "appId": "1:46796258106:web:186996496d075cb9866e03",
  "databaseURL": "https://personal-project-final-default-rtdb.europe-west1.firebasedatabase.app/"
}

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = '123456'

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['pass']
        name = request.form['name']
        username = request.form['username']
        stories = 0
        info = {"email": email, "password": password, "username": username, "name": name}

        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = user
            uid = user['localId']
            db.child("users").child(uid).set(info)
            # Initialize the stories node as an empty dictionary
            db.child("stories").child(uid).set({})
            return redirect(url_for('home'))
        except:
            return render_template('error.html')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['pass']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            return redirect(url_for('home'))
        except:
            return render_template('error.html')
    return render_template('login.html')

@app.route('/signout')
def signout():
    session['user']=None
    auth.current_user = None
    print("signed out user")
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        story = request.form['story']
        category = request.form['category']
        story_info = {"author": author, "title": title, "category": category, "story": story}
        try:
            user = session['user']
            uid = user['localId']
            db.child("stories").child(uid).push(story_info)
            return redirect(url_for('home'))
        except:
            return render_template('home.html')
    
    try:
        all_stories = db.child("stories").get().val()
        if all_stories:
            # Flatten the nested dictionary structure
            stories = {story_id: story for user_stories in all_stories.values() for story_id, story in user_stories.items()}
        else:
            stories = {}

        stories_json = jsonify(stories).get_data(as_text=True)
        return render_template('home.html', stories=stories, stories_json=stories_json)
    except:
        return render_template('home.html', stories={}, stories_json='{}')


@app.route('/get_stories', methods=['GET'])
def get_stories():
    try:
        user = session['user']
        uid = user['localId']
        stories = db.child("stories").child(uid).get().val()
        return jsonify(stories)
    except:
        return jsonify({})

@app.route('/create', methods=['GET', 'POST'])
def create():
    user = session['user']
    uid = user['localId']
    return render_template('create.html')

@app.route('/stories', methods=['GET', 'POST'])
def stories():
    user = session['user']
    uid = user['localId']
    stories = db.child("stories").child(uid).get().val()
    stories_json = jsonify(stories).get_data(as_text=True)
    info = db.child("users").child(uid).get().val()
    return render_template('stories.html',info = info,stories=stories, stories_json=stories_json)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = session['user']
    uid = user['localId']
    name = db.child("users").child(uid).get().val()['name']
    email = db.child("users").child(uid).get().val()['email']
    return render_template('prof.html',name= name,email=email)

@app.route('/edit', methods=['GET','POST'])
def edit():
    return render_template('edit.html')

@app.route('/delete/<story_id>', methods=['DELETE'])
def delete_story(story_id):
    try:
        user = session['user']
        uid = user['localId']
        stories = db.child("stories").child(uid).get().val()
        if story_id in stories:
            db.child("stories").child(uid).child(story_id).remove()
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "message": "Story not found"}), 404
    except:
        return render_template('error.html')
    return render_template('profile.html')

@app.route('/update' ,methods=['GET','POST'])
def update():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        username = request.form['username']
        info = {"name":name, "email":email,"password":password,"username":username}
        try:
            user = session['user']
            uid = user['localId']
            db.child("users").child(uid).update(info)
            return redirect(url_for('profile'))
        except:
            return render_template('error.html')
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
