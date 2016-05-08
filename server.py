from flask import Flask, render_template, redirect, session, request, flash 
#import the Connector function
from mysqlconnection import MySQLConnector 
#the "re" module will let us perfrom some regular expression operations
import re
#create a regular expression object that we can use operations on 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
from mysqlconnection import MySQLConnector 
app = Flask(__name__)
app.secret_key = 'IamSecret'
mysql = MySQLConnector(app, 'email_val_db')
print mysql.query_db("SELECT * FROM users")

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/process', methods=['POST'])
def success():
	#check if the form is empty or not 
	session['user-first-name'] = request.form['first_name']
	session['user-last-name'] = request.form['last_name']
	session['user-email'] = request.form['email']

	if (len(request.form['email']) < 1): 
		flash("Please tell me what your email")
	elif not EMAIL_REGEX.match(request.form['email']): #check email
		flash("Please input a valid email")
	else:
		# start mySQL insert
		query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at)  VALUES (:firstname, :lastname, :user, NOW(), NOW())"
		data = {
				'firstname': request.form['first_name'],
				'lastname': request.form['last_name'],
				'user': request.form['email'],
				}
		mysql.query_db(query, data)
		# end mySQL insert
		# start mySQL select
		user_list_query = "SELECT * FROM users"
		email_list = mysql.query_db(user_list_query)
		# end mySQL select
		return render_template('/processed.html', firstname = session['user-first-name'], email=session['user-email'], user_list=email_list)
	return render_template('/index.html')

@app.route('/deleted', methods=['POST'])
def deleteUser():
	session['deleted-email'] = request.form['deleteemail']
	query = "DELETE FROM users WHERE email = :email"
	data = {
			'email': request.form['deleteemail'],
			}
	mysql.query_db(query, data)
	return render_template('/deleted.html', deletedemail = session['deleted-email'])

@app.route('/clear')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect('/')


app.run(debug=True)