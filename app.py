from flask import Flask, render_template, redirect, session, request, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = "secrect key homie or I'll Mortal Combat you"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/register', methods=["post"]) # Registering User
def register():
    mysql = connectToMySQL('ArtistSite')
    data = {
    "fn" : request.form["firstname"],
    "ln" : request.form["lastname"],
    "em" : request.form["email"],
    "pw" : request.form["password"],
    "pw_cnf" : request.form["password_confirm"],
    }
    err = []
    if len(data['fn']) < 2:
        err.append("First name must be 2 characters or more")
        print('First name validation check')

    if len(data['ln']) < 2:
        err.append("Last name must be 2 characters or more")
        print('Last name validation check')

    if not EMAIL_REGEX.match(data['em']):
        err.append('Please enter a valid email')
        print('Email validation check')

    if len(data['pw']) < 8: # password check
        err.append('Password less the 8 characters')
        print('Password check')

    if not data['pw'] == data['pw_cnf']: # rechecking password
        err.append('Passwords need to match')
        print('Confirmed password check')

    if len(err) > 0:
        for i in err:
            flash(i)
    else:
        data['pw'] = bcrypt.generate_password_hash(data['pw'])
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(fn)s, %(ln)s, %(em)s, %(pw)s )"
        query_result = mysql.query_db(query, data)
        session['firstname'] = data["fn"]
        session['uid'] = query_result
        return redirect('/welcome_to_site')

    return redirect('/')



@app.route('/login', methods=["post"])
def login():
    mysql = connectToMySQL('ArtistSite')

    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form['email'], "password" : request.form['password']}
    print(data)
    result = mysql.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['uid'] = result[0]['id']
            session['firstname'] = result[0]["first_name"]
            return redirect('/welcome_to_site')
    flash("Login failed")
    return redirect('/')

@app.route('/welcome_to_site')  # Welcome to site html page//rendered route
def welcome_Homies():
    return render_template('home.html')

@app.route('/merch')   # Store html page//rendered route   
def merchandise():
    return render_template('store.html')

@app.route('/tours')
def tourDates():
    return render_template('tours.html')    # Tours html page//rendered route 

@app.route('/listen_to_music')
def listen_to_music():
    return render_template('listen.html')   # Listen to the album page//rendered route 



if __name__ == "__main__":
    app.run(debug=True)