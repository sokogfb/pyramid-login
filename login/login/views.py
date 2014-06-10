from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
import sqlite3 as lite
import bcrypt

#Salt for bcrypt. Generated with 10 rounds
salt = "$2a$10$hjrVZN2MLUfNxDajPgNl.O"


# Page: Home
# Shows the home page with login and register buttons
@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
	if(request.session.get('logged_in')):
		#User is logged in, don't show the page
		return HTTPFound(location=request.route_url('account'))
	#if logged in

	return {}
#home


# Page: Account
# Shows the account page and logout button
@view_config(route_name='account', renderer='templates/account.pt')
def account(request):
	if(not(request.session.get('logged_in'))):
		#User is logged in, don't show the page
		return HTTPFound(location=request.route_url('login'))
	#if logged in

	user_id = request.session.get('user_id') #Get user_id that was saved in session 
	con = lite.connect('login.db')
	with con: 
		cur = con.cursor() #Grab the cursor
		user = (user_id,) #Create the tuple for the query 
		cur.execute("SELECT * FROM users WHERE `id`=?", user) #SQL Injection? Nope! 
		user = cur.fetchone() #Fetch the first user returned 

		if(user == None): #user is not found? That's odd. Lets log them out
			return HTTPFound(location=request.route_url('logout'))
		else:
			return {"username": user[1]} #Hello, User!
		#if user
#account


# Page: Login
# Shows the login page
@view_config(route_name='login', renderer="templates/login.pt")
def login(request):

	if(request.session.get('logged_in')):
		#User is logged in, don't show the page
		return HTTPFound(location=request.route_url('home'))
	#if logged in

	if(request.method == "POST"):

		username = request.POST.get('username')
		password = request.POST.get('password')

		#Connect to SQLite
		con = lite.connect('login.db')
		with con:
			cur = con.cursor() #Grab the cursor
			user = (username, password) #User tuple to query the database
			cur.execute("SELECT * FROM users WHERE `username`=? AND `password`=?", user)
			user = cur.fetchone() #Get the first user for that query

			if(user == None): #Username or password incorrect? Show them an error!
				return {"error": "Username and Password combination is not valid", "username": username, "salt": salt}
			else: #Logged in
				#Set the session accordingly
				request.session['logged_in'] = True
				request.session['user_id'] = user[0]
				return HTTPFound(location=request.route_url('account')) #Redirect them to their account page
			#if user
	else:
		return {"username": "", "salt": salt}
#login


# Page: Logout
# Clears user session and redirects them
@view_config(route_name='logout')
def logout(request):
	request.session['logged_in'] = False
	request.session['user_id'] = None
	return HTTPFound(location=request.route_url('login'))
#logout


# Page: Register
# Shows the register page
@view_config(route_name='register', renderer="templates/register.pt")
def register(request):

	#Check user logged in
	if(request.session.get('logged_in')):
		#User is logged in, don't show the page
		return HTTPFound(location=request.route_url('account'))
	#if logged in


	#Check Request Method
	if(request.method == "POST"):
		#Validate Request
		username = request.POST.get('username')
		password = request.POST.get('password')

		if(len(username) < 4):
			return {"error": "Username must be at least 4 characters", "username": username, "salt": salt}
		if(len(password) < 8):
			return {"error": "Passowrd must be at least 8 characters", "username": username, "salt": salt}
		if(len(salt) == 0):
			#Bad salt?
			return {"error": "Bad Salt", "username": username, "salt": salt}
		#/Validate Request

		#Connect to the database
		con = lite.connect('login.db')
		with con:
			cur = con.cursor() #Grab the cursor

			#Check if username is taken already
			user = (username,) #User tuple
			cur.execute("SELECT * FROM users WHERE `username`=?", user)

			#Username not taken
			if(cur.fetchone() == None):
				#user not found - lets create it!
				user = (username, password, False)
				cur.execute("INSERT INTO users VALUES(null, ?, ?, ?)", user)

				#Set the session accordingly
				request.session['logged_in'] = True
				request.session['user_id'] = cur.lastrowid

				#Redirect them to account page
				return HTTPFound(location=request.route_url('account'))

			#Username taken - let them know
			else: 
				return {"error": "Username taken", "username": username, "salt": salt}

	else: #it's a GET request
		return {"username": "", "salt": salt}
#register


# Page: Admin
# Shows the admin page
@view_config(route_name='admin', renderer='templates/admin.pt')
def admin(request):
	if(not(request.session.get('logged_in'))):
		#User is logged in, don't show the page
		return HTTPFound(location=request.route_url('login'))
	#if logged in

	user_id = request.session.get('user_id') #Get user_id that was saved in session 
	con = lite.connect('login.db')
	with con: 
		cur = con.cursor() #Grab the cursor
		user = (user_id,) #Create the tuple for the query 
		cur.execute("SELECT * FROM users WHERE `id`=?", user) #SQL Injection? Nope! 
		user = cur.fetchone() #Fetch the first user returned 

		if(user == None): #user is not found
			return HTTPFound(location=request.route_url('logout'))
		else:

			if(user[3] != True): #User is NOT admin. Redirect to normal account page
				return HTTPFound(location=request.route_url('account'))
			else:
				cur.execute("SELECT * FROM users")
				allusers = cur.fetchall() #Fetch all users
				return {"username": user[1], "users": allusers}
		#if user
#admin
