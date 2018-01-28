from bottle import route, run, template, request
import psycopg2
import json

# Name of BBall Court: Basketball Court


conn = psycopg2.connect(
	dbname="fields", user="sportsclub2018", password="tamuhack2018",
	host='sportsclub2018.cbb3xkufzgzy.us-west-2.rds.amazonaws.com', port=5432)

c = conn.cursor()


@route('/getaddress')
def get_address():
	return template("{{zip_code}}", zip_code=000000)


@route('/updatebaseball')
def update_baseball():
	"""
	We need a number of variables. This is the function that will continue
	the update of the status of a current field
	"""
	condition = request.forms.get("condition")
	weather = request.forms.get("weather")
	cost = request.forms.get("cost")
	shelter = request.forms.get("shelter")
	turf = request.forms.get("turf")
	name = request.forms.get('name')

	update = (condition, weather, cost, shelter, turf, name)

	with conn:
		c.execute(
			"""
			UPDATE baseball_field
			SET 
			condition = %s,
			weather = %s,
			cost = %s,
			shelter = %s,
			turf = %s
			WHERE name = %s
			""", update
		)


@route('/updatebasketball')
def update_basketball():
	"""
	We need a number of variables. This is the function that will continue
	the update of the status of a current field

	"""
	condition = 4
	weather = 4
	cost = 2
	shelter = True
	floor_type = "Wood"
	name = "Basketball Court"
	full_court = True
	rim_cond = 3

	# condition = request.forms.get("condition")
	# weather = request.forms.get("weather")
	# cost = request.forms.get("cost")
	# shelter = request.forms.get("shelter")
	# floor_type = request.forms.get("floor_type")
	# name = request.forms.get("name")
	# full_court = request.forms.get("full_court")
	# rim_cond = request.forms.get("rim_cond")

	update = (
		condition, weather, cost, shelter, floor_type,
		full_court, rim_cond, name)

	with conn:
		c.execute(
			"""
			UPDATE basketball_court
			SET 
			condition = %s,
			weather = %s,
			cost = %s,
			shelter = %s,
			floor_type = %s,
			full_court = %s,
			rim_cond = %s
			WHERE name = %s
			""", update
		)


# @route('/createbasketball')
# def create_baseketball():
# 	"""
# 	We need a number of variables. This is the function that will continue
# 	the update of the status of a current field
# 	"""
# 	condition = 5
# 	weather = 3
# 	cost = 1
# 	shelter = True
# 	floor_type = "Wood"
# 	name = "Basketball Court"
# 	full_court = True
# 	rim_cond = 4
#
# 	update = (
# 		condition, weather, cost, shelter, floor_type,
# 		full_court, rim_cond, name)
#
# 	with conn:
# 		c.execute(
# 			"""
# 			INSERT INTO basketball_court
# 			VALUES
# 			condition = %s,
# 			weather = %s,
# 			cost = %s,
# 			shelter = %s,
# 			floor_type = %s,
# 			full_court = %s,
# 			rim_cond = %s,
# 			name = %s
# 			""", update
# 		)


@route('/getupdate')
def getupdate():
	"""
	This is what will run when we we reload the page that the use will see to
	check up on the status of a field
	"""

	requestinfo = {}

	with conn:
		c.execute(
			"""
			SELECT * FROM basketball_court
			WHERE name = 'Basketball Court'
			"""
		)
		values = c.fetchone()

		columns = [
			"condition", "weather", "cost", "shelter", "floor_type",
			"full_court", "rim_cond", "name"]

		for col, val in zip(columns, values):
			requestinfo[col] = val

		json_request = json.dumps(requestinfo)
		print(json_request)

		return json_request


@route('/followup')
def followup():
	"""
	This is the form that is filled out when we follow up with them
	Questions:
	1. How was the field (Send to condition)
	2. Would you come back? (??? Where do we put this information?
	What do we do with it? Do we display it?)
	3. Rating (INT)

	Need:
	Name of the Field

	We want to display to users looking up how others have answered these
	follow up questions
	"""

	name_of_field = request.forms.get("name_of_field")
	type_of_field = request.forms.get("type_of_field")
	condition = request.forms.get("condition")
	rating = request.forms.get("rating")

	with conn:
		# This is so that we can get the average ratings
		# of every place that we have and display to the user what
		# other people think of the place
		c.execute(
			"""
			INSERT INTO ratings (name_of_field, rating)
			VALUES (%s, %s)
			""", (name_of_field, rating)
		)

		# This will save the condition of the field (as an integer). We want
		# to display the average ratings to users who see the page
		c.execute(
			"""
			INSERT INTO %s (condition)
			VALUES (%s)
			""", (type_of_field, condition)
		)


@route('/signup')  # post to /login
def signup():
	"""
	Gets the users information and saves it to the
	database: SportsClub
	table: user_information
	"""
	# ident = request.forms.get('identification')
	# username = request.forms.get('username')
	# first_name = request.forms.get('first_name')
	# last_name = request.forms.get('last_name')
	# password = request.forms.get('password')
	# email = request.forms.get('email')

	# MOCK
	ident = 123456789
	username = "Username"
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

		# c.execute(
		# 	"SELECT * FROM user_information"
		# )
		# print(c.fetchall())

		# c.execute(
		# 	"DELETE FROM user_information"
		# )


@route('/login')
def login():
	"""
	This function will run on the login page
	"""
	# username = request.forms.get('username')
	# password = request.forms.get('password')

	# MOCK
	username = "Username"
	password = "Password"

	feed = (username, password)

	with conn:
		c.execute(
			"""
			SELECT first_name, last_name FROM user_information 
			WHERE
			username = %s AND
			password = %s
			""", feed
		)

		first_name, last_name = c.fetchone()

	return template(
		'{{first_name}},{{last_name}}',
		first_name=first_name, last_name=last_name)


@route("/delete")
def delete_entries():
	print("Deleting user_information table...")
	c.execute(
		"DELETE FROM basketball_court"
	)


# @route('/createtennis')
# def create_tennis():
# 	"""
# 	We need a number of variables. This is the function that will continue
# 	the update of the status of a current field
# 	"""
# 	# condition = request.forms.get("condition")
# 	# weather = request.forms.get("weather")
# 	# cost = request.forms.get("cost")
# 	# shelter = request.forms.get("shelter")
# 	# turf = request.forms.get("turf")
# 	# name = request.forms.get('name')
#
# 	condition = 3
# 	weather = 4
# 	cost = 3
# 	shelter = False
# 	net_cond = 3
# 	name = "Tennis Court"
#
# 	update = (condition, weather, cost, shelter, net_cond, name)
#
# 	with conn:
# 		c.execute(
# 			"""
# 			INSERT INTO tennis_fields
# 			VALUES
# 			condition = %s,
# 			weather = %s,
# 			cost = %s,
# 			shelter = %s,
# 			ned_cont = %s
# 			WHERE name = %s
# 			""", update
# 		)


# @route('/createsoccer')
# def create_soccer():
# 	"""
# 	We need a number of variables. This is the function that will continue
# 	the update of the status of a current field
# 	"""
# 	condition = request.forms.get("condition")
# 	weather = request.forms.get("weather")
# 	cost = request.forms.get("cost")
# 	shelter = request.forms.get("shelter")
# 	turf = request.forms.get("turf")
# 	name = request.forms.get('name')
#
# 	update = (condition, weather, cost, shelter, turf, name)
#
# 	with conn:
# 		c.execute(
# 			"""
# 			UPDATE baseball_field
# 			SET
# 			condition = %s,
# 			weather = %s,
# 			cost = %s,
# 			shelter = %s,
# 			turf = %s
# 			""", update
# 		)
#
#
# @route('/createswimmingpool')
# def create_swimmingpool():
# 	"""
# 	We need a number of variables. This is the function that will continue
# 	the update of the status of a current field
# 	"""
# 	# condition = request.forms.get("condition")
# 	# weather = request.forms.get("weather")
# 	# cost = request.forms.get("cost")
# 	# shelter = request.forms.get("shelter")
# 	# turf = request.forms.get("turf")
# 	# name = request.forms.get('name')
#
# 	condition = 2
# 	name = "Swimming Pool"
# 	weather = 4
# 	cost = 2
# 	shelter = False
# 	min_depth = 3
# 	max_depth = 11
# 	diving_board = True
# 	current_temp = 4
#
# 	update = (
# 		condition, weather, cost, shelter, min_depth, max_depth,
# 		diving_board, current_temp, name)
#
# 	with conn:
# 		c.execute(
# 			"""
# 			UPDATE baseball_field
# 			VALUES
# 			condition = %s,
# 			weather = %s,
# 			cost = %s,
# 			shelter = %s,
# 			min_depth = %s,
# 			max_depth = %s,
# 			diving_board = %s
# 			WHERE name = %s
# 			""", update
# 		)


run(host="localhost", port=4567)
# Our Domain name and port
