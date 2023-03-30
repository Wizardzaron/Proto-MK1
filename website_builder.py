#need to create db
#fallout cookbook jokes
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, abort
from datetime import timedelta


app = Flask(__name__)


@app.route('/signup', methods =['POST'])
def signup_post():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    msg = ''

	#password must be between 4 and 255
    if len(password) < 4 or len(password) > 255:
        msg = 'Password needs to be between 4 and 255 characters long.'
        return render_template('signup.html', msg = msg)
    
    #username must be between 4 and 255 
    if len(username) < 4 or len(username) > 255:
         msg= 'Username needs to be between 4 and 255 characters long.'
         return render_template('signup.html', msg = msg)
    #check if email is valid
    
    #username cannot include whitespace
    if any (char.isspace() for char in username):
         msg = 'Username cannot have spaces in it.'
         return render_template('signup.html', msg = msg)
    
    #email cannot include whitespace
    if any (char.isspace() for char in email):
         msg = 'Email cannot have spaces in it.'
         return render_template('signup.html', msg = msg)

    #username cannot already exist in database
    
    return render_template('welcome.html', msg = 'Signup successful.')

    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		
		
		
    #     cur.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
    #     conn.commit()
    #     account = cur.fetchone()
    #     if account:
			
	# 		session.permanent = True
	# 		session['loggedin'] = True
	# 		session['id'] = account['id']
	# 		session['username'] = account['username']
	# 		msg = 'Logged in successfully !'
	# 		return render_template('index.html', msg = msg)
	# 	else:
	# 		msg = 'Incorrect username / password !'
	# return render_template('login.html', msg = msg)
        
    # con = sqlite3.connect("userdata.db")
    # cur = con.cursor()
    # #request.form used on post html pages
    

    # cur.close()



@app.route('/signup', methods =['GET'])
def signup_get():
    return render_template('signup.html')

@app.route('/')
@app.route('/welcome', methods =['GET', 'POST'])
def welcome():
    
    return render_template('welcome.html')

if __name__ == "__main__":
	app.run()
        

