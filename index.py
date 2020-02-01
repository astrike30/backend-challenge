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
		print(request.json)
		write_new_club(request.json)
		return 'OK', 200

@app.route('/api/user/<string:username>')
def users(username):

	user = get_user(username)
	
	if user is None:
		return "User does not exist.", 404
	else:
		return jsonify(vars(user))

	return username


if __name__ == '__main__':
    app.run()
