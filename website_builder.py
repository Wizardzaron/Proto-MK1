#need to create db
#fallout cookbook jokes
from flask import Flask, render_template, request, redirect, url_for, session, abort
from datetime import timedelta


app = Flask(__name__)

@app.route('/')
@app.route('/welcome')
def begin():
    
    return render_template('index.html')

if __name__ == "__main__":
	app.run()