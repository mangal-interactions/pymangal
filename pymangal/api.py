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
        # We don't want the URL to end with a trailing slash
        # (if only because it makes things simpler after)
        if url[-1:] == '/':
            url = url[-1:]
        # Now we create the URL property
        self.root = url
        self.url = self.root + '/api/v1/'
        # We establish first contact with the API
        # Simply enough, we try to reach the root, and check the response code
        API = re.get(self.url, auth = auth)
        if not API.status_code == 200 :
            raise ValueError("The URL you provided ("+url+") gave a "+str(API.status_code)+" status code")
        self.resources = API.json().keys()
        # For each resource, we need to know which verbs are available
        allowed_verbs = {}
        for resource in self.resources:
            schema = self.root + API.json()[resource]['schema']
            schema_request = re.get(schema)
            if schema_request.status_code != 200 :
                raise ValueError("The schema for resource "+resource+" is not available")
            if not 'allowed_detail_http_methods' in schema_request.json():
                raise KeyError("The API do not give a list of allowed methods")
            allowed_verbs[resource] = schema_request.json()['allowed_detail_http_methods']
        self.verbs = allowed_verbs
