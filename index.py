from flask import Flask, request, jsonify
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
from users import * # Functions for interacting with user signup etc


app = Flask(__name__)

@app.route('/')

def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/api/clubs', methods=['GET', 'POST'])
def clubs():
	"""
	If a get request, return all of the stored clubs.
	If a post request, add or update the specified clubs
	"""
	if request.method == 'GET':
		return jsonify(read_json())
	elif request.method == 'POST':

		name = request.json["name"]
		description = request.json["description"]
		categories = request.json["categories"]

		if write_new_club(name, description, categories):
			return jsonify({"message": "Created new club"}), 200
		else:
			return jsonify({"message": "Club already exists, added updated information"})

@app.route('/api/user/<string:username>')
def users(username):
	"""
	Return all info for specified user at specified route paramater.
	"""
	user = get_user(username)
	
	if user is None:
		return jsonify({"message": "error"})
	else:
		json = vars(user)
		del json["passwordHash"] # remove all sensitive info from user
		del json["token"]
		del json["token_expiry"]
		return jsonify(json)

	return username

@app.route('/api/favorite', methods=['POST'])
def favourite():
	"""
	Flip the favourite state of a club for a given user.
	If the user has already favourited the club, then unfavourite it,
	otherwise favourite the club.
	"""

	token = request.json['token']
	user = request.json['user']
	club = request.json['club']

	if validate_token(user, token):
		if not flip_user_fav(user, club):
			inc_dec_fav_count(club, +1)
			return jsonify({"message": "Added favourite"})
		else:
			inc_dec_fav_count(club, -1)
			return jsonify({"message": "Removed favourite"})
	else:
		return jsonify({"message": "Invalid Token"})
	

@app.route('/api/signup', methods=['POST'])
def signup():
	"""
	Sign the the user up with given information. Return an error if username already exists.
	"""
	username = request.json['username']
	password = request.json['password']
	name = request.json['name']
	year = request.json['year']

	if get_user(username) is None:
		token = write_user(username, name, year, [], password)
		return jsonify({"message": "Signed up user", "token": token})
	else:
		return jsonify({"message": "User exists"})


@app.route('/api/token')
def token():
	"""
	Generate a new token for the specified user and password.
	Return an error if username or password is wrong. 
	"""
	username = request.form['username']
	password = request.form['password']

	token = get_token(username, password)

	if token:
		return jsonify({"message": "Generated new token successfully", "token": token})
	else:
		return jsonify({"message": "Incorrect username or password"})

@app.route('/api/comment', methods=["POST", "GET"])
def comment():
	"""
	Return all comments for a specific club if a get request.
	If a post request, then add a comment from a specific user if their token is correct and club exists.
	"""
	if request.method == 'POST':
		token = request.json['token']
		user = request.json['user']
		club = request.json['club']
		comment = request.json['comment']
		if validate_token(user, token):
			if add_club_comment(user, club, comment):
				return jsonify({"message": "Added comment successfully"})
			else:
				return jsonify({"message": "Club does not exist"})
		else:
			return jsonify({"message": "Invalid token, it may be expired, try requesting a new one."})
	else:
		club = request.args["club"]
		comments = get_all_comments()
		if club in comments.keys():
			return jsonify(comments[club])
		else:
			return jsonify({"message": "That club does not exist."})


if __name__ == '__main__':
    app.run()






