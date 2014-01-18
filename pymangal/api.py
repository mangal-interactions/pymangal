import json
import requests as re

class mangal:
    """This class will handle connection to the API.

    Args:
        url (str) : The URL of the api
        usr (str) : An optional username
        pwd (str) : An optional password

    Attributes
    url : The URL of the API + suffix
    resources : A list of the resources

    >>> mg = mangal(url='http://mangal.uqar.ca')

    """

    def __init__(self, url='http://mangal.uqar.ca', usr=None, pwd=None):
        auth = None
        # We check that the URL is a string
        if not isinstance(url, str):
            raise TypeError("The URL must be a string")
        # Let's check a bunch of things about the username and password
        if (usr == None) and (pwd != None):
            raise ValueError("You must provide a username")
        if (usr != None) and (pwd == None):
            raise ValueError("You must provide a password")
        # Finally if all is well, we check the type and create a auth object
        if (usr != None) and (pwd != None):
            if isinstance(usr, str) and isinstance(pwd, str):
                auth = (usr, pwd)
            else :
                raise TypeError("Both the password and the username must be strings")
        # We want the URL to end with a trailing slash
        if not url[-1:] == '/':
            url += '/'
        # Now we create the URL property
        self.url = url + 'api/v1/'
        # We establish first contact with the API
        # Simply enough, we try to reach the root, and check the response code
        API = re.get(self.url, auth = auth)
        if not API.status_code == 200 :
            raise ValueError("The URL you provided ("+url+") gave a "+str(API.status_code)+" status code")
        self.resources = API.json().keys()

