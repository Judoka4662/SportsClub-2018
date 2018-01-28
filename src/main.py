from bottle import route, run, template, request, post, get
import psycopg2


conn = psycopg2.connect(
	dbname="fields", user="sportsclub2018", password="tamuhack2018",
	host='sportsclub2018.cbb3xkufzgzy.us-west-2.rds.amazonaws.com', port=5432)

c = conn.cursor()


@route('/followup')
def followup():
	"""
	This is the form that is filled out when we follow up with them
	Questions:
	1. How was the field (Send to condition)
	2. Would you come back? (??? Where do we put this information?
	What do we do with it? Do we display it?)
	3. Rating (INT)
	"""

	pass


@route('/login')  # post to /login
def login():
	"""
	Gets the users information and saves it to the
	database: SportsClub
	table: user_information
	"""
	ident = request.forms.get('identification')
	username = request.forms.get('username')
	first_name = request.forms.get('first_name')
	last_name = request.forms.get('last_name')
	password = request.forms.get('password')
	email = request.forms.get('email')

	# MOCK
	ident = 123456789
	username = "Username123456789"
	first_name = "First Name"
	last_name = "Last Name"
	password = "Password"
	email = "Email"

	new_user = (ident, username, first_name, last_name, password, email)

	with conn:
		c.execute(
			"""INSERT INTO user_information 
			(ident, username, first_name, last_name, password, email) 
			VALUES (
			%s, %s, %s, %s, %s, %s
			)""", new_user)

		c.execute(
			"SELECT * FROM user_information"
		)
		print(c.fetchall())

		c.execute(
			"DELETE FROM user_information"
		)


def delete_entries():
		c.execute(
			"DELETE FROM user_information"
		)


# @route('/')
def get_login():
	print("Get_login")
	with conn:
		c.execute(
			"SELECT * FROM user_information"
		)

		print(c.fetchall())


run(host="localhost", port=4567)
# Our Domain name and port
