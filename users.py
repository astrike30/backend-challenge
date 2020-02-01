import json

class User:

	def __init__(self, username, name, year, interests):
		self.username = username
		self.name = name
		self.year = year
		self.interests = interests

def write_user(username, name, year, interests):

	user = {"name": name, "year": year, "interests": interests}
	with open('users.json') as json_file:
		existing = json.load(json_file)
		existing[username] = user
		with open('users.json', 'w') as outfile:
			json.dump(existing, outfile)


def get_user(username):

	with open('users.json') as json_file:
		existing = json.load(json_file)

		if username not in existing.keys():
			return None

		user = existing[username]
		return User(username, user["name"], user["year"],
					user["interests"])



if __name__ == "__main__":
	write_user("jen", "Jennifer", 2023, ["Programming", "Sports"])
