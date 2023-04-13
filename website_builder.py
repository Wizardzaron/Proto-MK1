import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, abort, current_app, jsonify
from datetime import timedelta
import datetime
from flask import send_from_directory
from functools import wraps
# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager
from email_validator import validate_email, EmailNotValidError
import os
import sys
import jwt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
#app.permanent_session_lifetime = timedelta(minutes=10)

#Setting up JWT extension
# app.config["JWT_SECRET_KEY"] = "Matt's Mind"
# jwt = JWTManager(app)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = 'userimages'

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = session.get('Authorization') #https://127.0.0.1:5000/route?token=afhftdchbiuig

#         if not token:
#             return jsonify({'message' : 'Token is missing!'}), 401
        
#         try:
#             data = jwt.encode().decode(token, app.config['SECRET_KEY'])
#         except:
#             return jsonify({'message' : 'Token is invalid !!'}), 401
        
#         return f(*args, **kwargs)
#     return decorated



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
         msg = 'Username needs to be between 4 and 255 characters long.'
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
    insertNewUser = """INSERT INTO info (username,pass,phonenumber,email) VALUES (?,?,?,?)"""
    cur.execute(insertNewUser, [username, password, phonenumber, email])

    newUserId = cur.lastrowid

    print(newUserId)

    cur.close()

    return render_template('welcome.html', msg = 'Signup successful. ' + str(newUserId))

@app.route('/publish', methods = ['GET'])
#@token_required
def publish_get():
     
    msg = ''
        #current_user = get_jwt_identity()
    
        #return render_template('welcome.html', msg = str(e))

    session.pop('logged_in', None)
    return render_template('publish.html')


@app.route('/publish', methods = ['POST'])
#@jwt_required()
def publish_post():
    #image = request.files['imagefile']
    description = request.form['description']
    title = request.form['title']
    image = request.files['file']
    
    if len(description) < 50:
         msg= 'Your review must be longer than 50 characters long'
         return render_template('publish.html', msg = msg)



    #splits apart the file name and grabs the extenstion 
    file_ext = os.path.splitext(image.filename)[1]
    
    #current_app can be used to access data about the running application, including the configuration (such as UPLOAD_EXTENSIONS)

    if file_ext not in app.config['UPLOAD_EXTENSIONS']:
        return render_template( 'publish.html' , msg = 'This file type is not supported.')

# error from next line
    image.save(os.path.join(app.config['UPLOAD_PATH'], image.filename))

    pathToImage = "/user_image/"  # '/Users/ryan0\OneDrive\Desktop\WebsiteBuilder\Wizardzaron.github.io'

    conn = sqlite3.connect('userdata.db')
    
    cur = conn.cursor()

    insertNewReview = """INSERT INTO reviews (reveiw, title, creator_id, image_name) VALUES (?, ?, ?, ?)"""
    conn.execute(insertNewReview, [description, title, 1, image.filename])
    conn.commit()


    rows = []
    try:
         
        getReviews =  '''SELECT  id, title, reveiw, image_name, creator_id FROM reviews'''
        cur.execute(getReviews)
        reviews = cur.fetchall()

        columns = ('id', 'title', 'reveiw', 'image_name', 'creator_id')

        #creating dictionary
        for row in reviews:
            print(f"trying to serve {row}", file=sys.stderr)
            rows.append({columns[i]: row[i] for i, _ in enumerate(columns)})
            print(f"trying to serve {rows[-1]}", file=sys.stderr)

    except Exception as e:
        msg = 'Query Failed: %s\nError: %s' % (getReviews, str(e))
        return render_template('home.html', msg = msg, reviews = [])
    
    finally:    
        conn.close()
        
    pathToImage = 'user_image/'
    return render_template('home.html', msg = 'Welcome Guest', rows = rows, pathToImage = pathToImage)




@app.route('/login', methods =['POST'])
def login():
    
    #For the new /login route we need to specifiy the POST method as well as GET so that end users can send a POST request 
    # with their login credentials to that /login endpoint


    try:
        if 'username' in request.form and 'password' in request.form:

            msg = ''

            username = request.form['username']        
            password = request.form['password']

            token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])
            session['Authorization'] = token

            session['loggedin'] = True
            
            conn = sqlite3.connect('userdata.db')
            cur = conn.cursor()


            #COUNT() means that it returns the number of rows that matches a specified criterion
            getCountByUsernameAndPassword = '''SELECT COUNT() FROM info WHERE username = ? AND pass = ?'''
            cur.execute(getCountByUsernameAndPassword,[username,password])
            countOfUsernameAndPassword = cur.fetchone()
            
            if countOfUsernameAndPassword[0] == 0:
                msg = 'Account does not exist.'
                return render_template('welcome.html', msg = msg)
            

            #accessToken = create_access_token(identity = username)
            #session['accessToken'] = accessToken
            session['logged_in'] = True
            #return jsonify(access_token=accessToken)
    except Exception as e:
        print('An error occured:', str(e))
        return
    #sessions carry data over the website


    
    rows = list()
    
    print(f"trying to serve", file=sys.stderr)

    try:
         
        getReviews =  '''SELECT  id, title, reveiw, image_name, creator_id FROM reviews'''
        cur.execute(getReviews)
        reviews = cur.fetchall()

        columns = ('id', 'title', 'reveiw', 'image_name', 'creator_id')

        #creating directory
        for row in reviews:
            print(f"trying to serve {row}", file=sys.stderr)
            rows.append({columns[i]: row[i] for i, _ in enumerate(columns)})
            print(f"trying to serve {rows[-1]}", file=sys.stderr)

    except Exception as e:
        msg = 'Query Failed: %s\nError: %s' % (getReviews, str(e))
        return render_template('home.html', msg = msg, reviews = [])
        
    #try:
         
    #    getReviews =  'SELECT id, title, reveiw, image_name, creator_id FROM reviews'
    #    cur.execute(getReviews)
    #    reviews = cur.fetchall()

    #except Exception as e:
    #    msg = 'Query Failed: %s\nError: %s' % (getReviews, str(e))
    #    return render_template('home.html', msg = msg)
    
    #finally:    
   #     conn.close()

    #session['username'] = getCountByUsernameAndPassword['username']
    pathToImage = 'user_image/'
    return render_template('home.html', msg = 'Login successful. ', msg2 = 'Would you like to publish a review?', rows = rows, session = session, pathToImage = pathToImage)


@app.route('/user_image/<path:path>')
def send_user_image(path):
    print(f"trying to serve {path}", file=sys.stderr)

    return send_from_directory('userimages', path)

@app.route('/home', methods = ['GET'])
def home_page():
    session.pop('logged_in', None)

    conn = sqlite3.connect('userdata.db')
    
    cur = conn.cursor()
    rows = list()
    
    print(f"trying to serve", file=sys.stderr)

    try:
         
        getReviews =  '''SELECT  id, title, reveiw, image_name, creator_id FROM reviews'''
        cur.execute(getReviews)
        reviews = cur.fetchall()

        columns = ('id', 'title', 'reveiw', 'image_name', 'creator_id')

        #creating directory
        for row in reviews:
            print(f"trying to serve {row}", file=sys.stderr)
            rows.append({columns[i]: row[i] for i, _ in enumerate(columns)})
            print(f"trying to serve {rows[-1]}", file=sys.stderr)

    except Exception as e:
        msg = 'Query Failed: %s\nError: %s' % (getReviews, str(e))
        return render_template('home.html', msg = msg, reviews = [])
    
    finally:    
        conn.close()
        
    pathToImage = 'user_image/'
    return render_template('home.html', msg = 'Welcome Guest', rows = rows, pathToImage = pathToImage)




@app.route('/signup', methods =['GET'])
def signup_get():
    return render_template('signup.html')

@app.route('/')
@app.route('/welcome', methods =['GET', 'POST'])
def welcome():
     
    return render_template('welcome.html')

# @app.route("/admin", methods =['GET'])
# def admin():
#     msg = ''
#     if('username' in session and session['username'] == 'u1'):
#         return render_template('admin.html')
#     else:
#          msg = 'unauthorized user name'
#     return render_template('welcome.html', msg = msg)


if __name__ == "__main__":
	app.run()
        

