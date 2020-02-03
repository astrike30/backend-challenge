from flask import Flask, request, jsonify
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
from users import *


app = Flask(__name__)

@app.route('/')

def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/api/clubs', methods=['GET', 'POST'])
def clubs():
	if request.method == 'GET':
		return jsonify(get_clubs_json())
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

	user = get_user(username)
	
	if user is None:
		return jsonify({"message": "error"})
	else:
		json = vars(user)
		del json["passwordHash"]
		del json["token"]
		del json["token_expiry"]
		return jsonify(json)

	return username

@app.route('/api/favorite', methods=['POST'])
def favourite():
	if request.method == 'POST':

		token = request.json['token']
		user = request.json['user']
		club = request.json['club']

		if validate_token(user, token):
			if not flip_user_fav(user, club):
				inc_dec_fav_count(club, +1)
			else:
				inc_dec_fav_count(club, -1)
			return jsonify({"message": "OK"})
		else:
			return jsonify({"message": "error"})
	

@app.route('/api/signup', methods=['POST'])
def signup():
	username = request.json['username']
	password = request.json['password']
	name = request.json['name']
	year = request.json['year']

	if not get_user(username):
		token = write_user(username, name, year, [], password)
		return jsonify({"message": "success", "token": token})
	else:
		return jsonify({"message": "error"})


@app.route('/api/token')
def token():
	username = request.form['username']
	password = request.form['password']

	token = get_token(username, password)

	if token:
		return jsonify({"message": "success", "token": token})
	else:
		return jsonify({"message": "error"})

@app.route('/api/comment', methods=["POST", "GET"])
def comment():
	if request.method == 'POST':
		token = request.json['token']
		user = request.json['user']
		club = request.json['club']
		comment = request.json['comment']

		if validate_token(user, token):
			if add_club_comment(user, club, comment):
				return jsonify({"message": "success"})
			else:
				return jsonify({"message": "Club does not exist"})
		else:
			return jsonify({"message": "Invalid token, it may be expired, try requesting a new one."})


if __name__ == '__main__':
    app.run()






