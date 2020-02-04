# Penn Labs Server Challenge

## Documentation
For storing scraped scrapend club data, I decided to go with a JSON file. Reading from a plaintext file is sufficiently fast for an application like this. There are also no complex relations, so I'm able to store all the fields that I want. A full datatbase with SQLite or MySQL could be overkill. I also decided to store users in a JSON file for similiar reasons. If there were concurrent read and writes a db might be more appropriate.

All of the API endpoints return a standard JSON resonse with a message field. This indicates if there was an error or if a post request went through successfully.

For login, I decided to go with giving a hashed password to every user. This is stored in the user file, but is removed when a response is returned for a get request for a user. When a user signs in, they receive a token, this is then used for all post requests in the api. If the token is wrong an error is returned in the JSON response. The token has an associated expiry date, according to best practices. When this happens, the user must request a new token.

For user commenting, I decided to have a separate file where all of the comments are stored to keep the club json file from becoming too bloated. The club names are used as keys in comments.json and the comments themselves are stored as string in an array. The comments can be queried with a get request with the name of the club as a paramater.

### Additional Dependencies

- Passlib is used for creating hashes from plaintext passwords for security. It is also used to verify passwords when generating a new token.

## Running
Please run ```pipenv install``` to ensure that all dependencies are installed. ```scraper.py``` should also be run to scrape data and store it in ```clubs.json``` before the webserver is started. JSON files for users and comments have not been included in the ```.gitignore``` for conveinience. In a live implmentation, this would not be the case.