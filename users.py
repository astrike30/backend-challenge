import json
from passlib.hash import pbkdf2_sha256
import random
import time
import string

class User:
	"""
	Object for representing stored users.
	"""
	def __init__(self, username, name, year, interests, passwordHash, token, token_expiry,favs=[]):
		self.username = username
		self.name = name
		self.year = year
		self.interests = interests
		self.favourites = favs
		self.token = token
		self.passwordHash = passwordHash
		self.token_expiry = token_expiry # Indicates when a user's token expires.
		# For security a new token should be generated after a certain period.

def read_user_json():
	"""
	Write json to users file.
	"""
    with open('users.json') as json_file:
        return json.load(json_file)

def write_user_json(toWrite):
	"""
	Write user json to users file.
	"""
    with open('users.json', 'w') as outfile:
        json.dump(toWrite, outfile)

def write_user(username, name, year, interests, password ,favs=[]):
	"""
	Write a new user to the users json file.
	"""
	hashed = pbkdf2_sha256.hash(password) # Generate a hash from plaintext password given.
	token = secure_token() # Generate a new token for api calls.
	user = {
			"token": token, "token_expiry": int(time.time()) + 60*60*24*30, # lasts 30 days
			"password": hashed, "name": name, "year": year, 
			"interests": interests, "favourites": []
			}
	existing = read_json()
	existing[username] = user
	write_user_json(existing)
	return token

def secure_token():
	"""
	Generate a random 20 digit character sequence to be used as a token for api calls.
	"""
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))

def update_token(username):
	existing = read_json()
	existing["username"]["token"] = secure_token()
	existing["username"]["token_expiry"] = int(time.time()) + 60*60*24*30
	write_json(existing)
	return new_token

def validate_token(username, token):
	user = get_user(username)
	if user.token == token and user.token_expiry > time.time():
		return True
	else:
		return False

def get_token(username, password):
	user = get_user(username)

	if pbkdf2_sha256.verify(password, user["password"]):
		if (time.time() > user.token_expiry):
			return update_token(username)
		else:
			return user.token
	else:
		return None

def get_user(username):

	with open('users.json') as json_file:
		existing = json.load(json_file)

		if username not in existing.keys():
			return None

		user = existing[username]
		return User(username, user["name"], user["year"],
					user["interests"], user['password'], user["token"], 
					user["token_expiry"], favs=user["favourites"])

def flip_user_fav(username, club):
	existing = read_json()

	user = get_user(username)

	inc_dec = club in user.favourites

	if inc_dec:
		favs = existing[user.username]['favourites']
		del existing[user.username]['favourites'][favs.index(club)]
	else:
		existing[user.username]['favourites'].append(club)

	write_json(existing)
	return inc_dec

if __name__ == "__main__":
	write_user("jen", "Jennifer", 2023, ["Programming", "Sports"], "jen's password")
