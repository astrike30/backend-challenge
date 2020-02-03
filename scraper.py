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

    clubs = read_json()

    for i, club in enumerate(clubs):
        if club["name"] == clubname:
            print(clubs[i])
            print(clubs[i])
            clubs[i]["favourites"] += amt
            break
    write_json(clubs)

def read_json():
    with open('clubs.json') as json_file:
        return json.load(json_file)

def write_json(toWrite):
    with open('clubs.json', 'w') as outfile:
        json.dump(toWrite, outfile)


def write_new_club(name, description, categories):
    
    clubs = read_json()

    if name in [club["name"] for club in clubs]:
        return False

    club_json = {"name": name, "categories": categories, "description": description,
                "favourites": 0}

    clubs.append(club_json)

    write_json(clubs)
    return True

def add_favourites_field():
    """
    Adds a favourites field to the json of scraped data.
    """
    existing = read_json()

    if 'favourites' not in existing[0].keys():
        for club in existing:
            club['favourites'] = 0
    write_json(existing)
    print(existing[0])   

def create_comment_file():
    club = read_json()
    comment_dict = {}

    for club in clubs:
        comment_dict[club["name"]] = []

    with open('club_comments.json', 'w') as outfile:
        json.dump(comment_dict, outfile)

def add_club_comment(user, club, comment):

    with open('club_comments.json') as json_file:
        comments = json.load(json_file)
        if club in comments.keys():
            if comments[club] is None:
                 comments[club] = [user + ": " + comment]
            else:
                 comments[club].append(user + ": " + comment)
            with open('club_comments.json', 'w') as outfile:
                json.dump(comments, outfile)
            return True
        else:
            return False

if __name__ == "__main__":

    soup = soupify(get_clubs_html())
    clubs = [Club(get_club_name(x), get_club_tags(x),
                get_club_description(x)) for x in get_clubs(soup)]
    clubs = [vars(club) for club in clubs]
    print(clubs)
    write_new_club(clubs)

    add_favourites_field()
    create_comment_file()




