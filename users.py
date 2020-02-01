import json

class User:

	def __init__(self, username, name, year, interests, favs=[]):
		self.username = username
		self.name = name
		self.year = year
		self.interests = interests
		self.favourites = favs

def read_json():
    with open('users.json') as json_file:
        return json.load(json_file)

def write_json(toWrite):
    with open('users.json', 'w') as outfile:
        json.dump(toWrite, outfile)

def write_user(username, name, year, interests, favs=[]):

	user = {"name": name, "year": year, "interests": interests, "favourites": []}
	existing = read_json()
	existing[username] = user
	write_json(existing)


def get_user(username):

	with open('users.json') as json_file:
		existing = json.load(json_file)

		if username not in existing.keys():
			return None

		user = existing[username]
		return User(username, user["name"], user["year"],
					user["interests"], user["favourites"])

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
	write_user("jen", "Jennifer", 2023, ["Programming", "Sports"])
