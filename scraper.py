from bs4 import BeautifulSoup
import urllib.request
from club import Club
import json

def get_html(url):
    """
    Retrieve the HTML from the website at `url`.
    
    """
    return urllib.request.urlopen(url)

def get_clubs_html():
    """
    Get the HTML of online clubs with Penn.
    """
    url = 'https://ocwp.apps.pennlabs.org'
    return get_html(url)

def soupify(html):
    """
    Load HTML into BeautifulSoup so we can extract data more easily

    Note that for the rest of these functions, whenever we refer to a "soup", we're refering
    to an HTML document or snippet which has been parsed and loaded into BeautifulSoup so that
    we can query what's inside of it with BeautifulSoup.
    """
    return BeautifulSoup(html, "html.parser") 


def get_elements_with_class(soup, elt, cls):
    """
    Returns a list of elements of type "elt" with the class attribute "cls" in the
    HTML contained in the soup argument.

    For example, get_elements_with_class(soup, 'a', 'navbar') will return all links
    with the class "navbar". 

    Important to know that each element in the list is itself a soup which can be
    queried with the BeautifulSoup API. It's turtles all the way down!
    """ 
    return soup.findAll(elt, {'class': cls})

def get_clubs(soup):
    """
    This function should return a list of soups which each correspond to the html
    for a single club.
    """

    return get_elements_with_class(soup, 'div', 'box')

def get_club_name(club):
    """
    Returns the string of the name of a club, when given a soup containing the data for a single club.

    We've implemented this method for you to demonstrate how to use the functions provided.
    """
    elts = get_elements_with_class(club, 'strong', 'club-name')
    if len(elts) < 1:
        return ''
    return elts[0].text

def get_club_description(club):
    """
    Extract club description from a soup of 
    """
    elts = get_elements_with_class(club, 'em', '')
    if len(elts) < 1:
        return ''
    return elts[0].text

    return ''

def get_club_tags(club):
    """
    Get the tag labels for all tags associated with a single club.
    """

    div = get_elements_with_class(club, 'div', '')[0]
    if len(div) < 1:
        return []

    tags = get_elements_with_class(div, 'span', 'tag is-info is-rounded')

    return [tag.text for tag in tags]

def inc_dec_fav_count(clubname, amt):
    """
    Increment the the club favourite amount by either 1 or -1.
    """
    clubs = read_json()

    for i, club in enumerate(clubs):
        if club["name"] == clubname:
            print(clubs[i])
            clubs[i]["favourites"] += amt
            break # Stop loop when the club is found
    write_json(clubs)

def read_json():
    """
    Read all the json from the file and return it as a dict.
    """
    with open('clubs.json') as json_file:
        return json.load(json_file)

def write_json(toWrite):
    """
    Write a dictionary to the file as json.
    """
    with open('clubs.json', 'w') as outfile:
        json.dump(toWrite, outfile)


def write_new_club(name, description, categories):
    """
    Add a new club if no club with that name alread exists. If the club exists, then update
    its information.
    """
    clubs = read_json()

    if name in [club["name"] for club in clubs]: # if club already exists, update it

        for i, club in enumerate(clubs):
            if name == club["name"]:
                updated_club = clubs[i]
                updated_club["name"] = name
                updated_club["description"] = description
                updated_club["categories"] = categories
                del clubs[i]
                clubs.append(updated_club)
                break # stop when correct club is found

        write_json(clubs)
        return True
    else:      
        club_json = {"name": name, "categories": categories, "description": description,
                    "favourites": 0}
        clubs.append(club_json) # add new club if it doesn't exist
        write_json(clubs)

        existing_comments = get_all_comments()
        existing_comments[name] = [] # add the new club to the comments JSON file.

        return False

def add_favourites_field():
    """
    Adds a favourites field to the json of scraped data.
    """
    existing = read_json()

    if 'favourites' not in existing[0].keys(): # if the field has not already been added, add it.
        for club in existing:
            club['favourites'] = 0
    write_json(existing)

def create_comment_file():
    """
    Create the file that stores comments with all of the clubs that are in the clubs json file.
    """
    club = read_json()
    comment_dict = {}

    for club in clubs:
        comment_dict[club.name] = []

    with open('club_comments.json', 'w') as outfile:
        json.dump(comment_dict, outfile)

def add_club_comment(user, club, comment):
    """
    Add a new comment to an existing club.
    """
    with open('club_comments.json') as json_file:
        comments = json.load(json_file)
        if club in comments.keys():
            if comments[club] is None: # If there are no comments associated with the club Python returns None
                 comments[club] = [user + ": " + comment] 
            else:
                 comments[club].append(user + ": " + comment)
            with open('club_comments.json', 'w') as outfile:
                json.dump(comments, outfile)
            return True 
        else:
            return False # If the specified club name does not exist return False so an error can be specified to the api caller.

def get_all_comments():
    with open('club_comments.json') as json_file:
        return json.load(json_file)

if __name__ == "__main__":
    """
    Script should be run before the first time the webserver is started.
    """
    soup = soupify(get_clubs_html()) # scrape the web data
    clubs = [Club(get_club_name(x), get_club_tags(x),
                get_club_description(x)) for x in get_clubs(soup)] # put scraped web data into a List of users.

    [write_new_club(club.name, club.description, club.categories) for club in clubs] # write all of the scraped clubs to the json file.

    add_favourites_field() # Add a field for favourites to the json file.
    create_comment_file() # Add a json file for comments.




