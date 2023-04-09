#need to create db
#fallout cookbook jokes
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, abort, current_app
from datetime import timedelta
from flask import send_from_directory
from email_validator import validate_email, EmailNotValidError
import os

app = Flask(__name__)
app.secret_key = 'Sa_sa'

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']

@app.route('/signup', methods =['POST'])
def signup_post():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    phonenumber = request.form['phonenumber']
    msg = ''
    msg2 = ''


	#password must be between 4 and 255
    if len(password) < 4 or len(password) > 255:
        msg = 'Password needs to be between 4 and 255 characters long.'
        return render_template('signup.html', msg = msg)
    
    #username must be between 4 and 255 
    if len(username) < 4 or len(username) > 255:
         msg= 'Username needs to be between 4 and 255 characters long.'
         return render_template('signup.html', msg = msg)
    
    #check if email is valid

    #another way of doing if else statement

    try:
        # Check that the email address is valid.
        validation = validate_email(email)

        # Take the normalized form of the email address
        # for all logic beyond this point (especially
        # before going to a database query where equality
        # may not take into account Unicode normalization).  
        email = validation.email
    except EmailNotValidError as e:
        # Email is not valid.
        # The exception message is human-readable.
        return render_template('signup.html', msg = 'Email not valid: ' + str(e))


    #username cannot include whitespace
    if any (char.isspace() for char in username):
         msg = 'Username cannot have spaces in it.'
         return render_template('signup.html', msg = msg)
    
    #email cannot include whitespace
    if any (char.isspace() for char in email):
         msg = 'Email cannot have spaces in it.'
         return render_template('signup.html', msg = msg)

    #username cannot already exist in database
    conn = sqlite3.connect('userdata.db')
    
    # cursor object
    cur = conn.cursor()
    
    # to select all column we will use
    getCountByUsername = '''SELECT COUNT() FROM info WHERE username = ?'''
    cur.execute(getCountByUsername,[username])
    countOfUsername = cur.fetchone()

    if countOfUsername[0] != 0 :
         msg = 'Username already exists.'
         return render_template('signup.html', msg = msg)        

    #ready to insert into database
    insertNewUser = """INSERT INTO info (username,password,phonenumber,email) VALUES (?,?,?,?)"""
    conn.execute(insertNewUser, [username, password, phonenumber, email])
    conn.commit()

    cur.close()

    return render_template('welcome.html', msg = 'Signup successful. ')

@app.route('/publish', methods = ['POST'])
def publish_post():
    #image = request.files['imagefile']
    description = request.form['description']
    title = request.form['title']
    
    if len(description) < 50:
         msg= 'Your review must be longer than 50 characters long'
         return render_template('publish.html', msg = msg)



    #splits apart the file name and grabs the extenstion 
   # file_ext = os.path.splitext(image)[1]
    
    #current_app can be used to access data about the running application, including the configuration (such as UPLOAD_EXTENSIONS)

   # if file_ext not in current_app.config('UPLOAD_EXTENSIONS'):
    #    return render_template( 'publish.html' , msg = 'This file type is not supported.')

    conn = sqlite3.connect('userdata.db')
    
    cur = conn.cursor()

    insertNewUser = """INSERT INTO reviews (reveiws, title) VALUES (?, ?)"""
    conn.execute(insertNewUser, [description, title])
    conn.commit()

    cur.close()

    return render_template('home.html', msg = 'Review published')

@app.route('/login', methods =['GET', 'POST'])
def login():
    

    #For the new /login route we need to specifiy the POST method as well as GET so that end users can send a POST request 
    # with their login credentials to that /login endpoint


    try:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:


            msg = ''

            username = request.form['username']
            
            password = request.form['password']

            conn = sqlite3.connect('userdata.db')
            cur = conn.cursor()


            #COUNT() means that it returns the number of rows that matches a specified criterion
            getCountByUsernameAndPassword = '''SELECT COUNT() FROM info WHERE username = ? AND password = ?'''
            conn.commit()
            cur.execute(getCountByUsernameAndPassword,[username,password])
            
            countOfUsernameAndPassword = cur.fetchone()
            
            if countOfUsernameAndPassword[0] == 0:
                msg = 'Account does not exist.'
                return render_template('welcome.html', msg = msg)
    except Exception as e:
         print('An error occured:', str(e))
    
    #sessions carry data over the website
    
    session['logged_in'] = True

    try:
         
        getReviews =  '''SELECT title, reveiws FROM reviews'''
        cur.execute(getReviews)
        reviews = cur.fetchall()

    except Exception as e:
        msg = 'Query Failed: %s\nError: %s' % (getReviews, str(e))
        return render_template('home.html', msg = msg)
    
    finally:    
        conn.close()

    return render_template('home.html', msg = 'Login successful. ', msg2 = 'Would you like to publish a review?', reviews = reviews)


@app.route('/home', methods = ['GET'])
def home_page():
    session.pop('logged_in', None)

    conn = sqlite3.connect('userdata.db')
    
    cur = conn.cursor()
    
    try:
         
        getReviews =  '''SELECT title, reveiws FROM reviews'''
        cur.execute(getReviews)
        reviews = cur.fetchall()

    except Exception as e:
        msg = 'Query Failed: %s\nError: %s' % (getReviews, str(e))
        return render_template('home.html', msg = msg)
    
    finally:    
        conn.close()

    return render_template('home.html', msg = 'Welcome Guest', reviews = reviews)


@app.route('/publish', methods = ['GET'])
def publish_get():
     session.pop('logged_in', None)
     return render_template('publish.html')

@app.route('/signup', methods =['GET'])
def signup_get():
    return render_template('signup.html')

@app.route('/')
@app.route('/welcome', methods =['GET', 'POST'])
def welcome():
     
    return render_template('welcome.html')

if __name__ == "__main__":
	app.run()
        

