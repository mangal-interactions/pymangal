import json
import requests as re

class mangal:
    """Handles connection to the API

    This is the main class used by ``pymangal``. When called, it will return
    an object with all methods and attributes required to interact with
    the database.

    """

    def __init__(self, url='http://mangal.uqar.ca', usr=None, pwd=None):
        """Creates an instance of a ``mangal`` class

        Args:
            url (str): The URL of the site with the API
            usr (str): Your username on the server
            pwd (str): Your password on the server

        Returns:
            An object of class ``mangal``

        .. note::
            At this point, it is assumed that the suffix is
            ``/api/v1`` - that will be changed in future version
        """
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
        self.auth = auth
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

    def List(self, resource='dataset', filters=None, autopage=False):
        """ Lists all objects of a given resource type, according to a filter

        Args:
            resource (str): A type of resource available
            filters (str): A string giving the filtering parameters
            autopage (true): Whether to keep on listing until all objects are retrieved

        Returns:
            objects (array): An array of objects, each being a ``dict``
        """
        list_objects = []
        if not isinstance(autopage, bool):
            raise TypeError("autopage must be a boolean")
        if not isinstance(resource, str):
            raise TypeError("resource must be a string")
        if not filters == None:
            if not isinstance(filters, str):
                raise TypeError("filters must be a string")
        if not resource in self.resources:
            raise ValueError("This type of resource is not available")
        list_url = self.url + resource
        list_request = re.get(list_url, auth=self.auth)
        if list_request.status_code != 200 :
            raise ValueError("There was an error in listing the objects")
        list_content = list_request.json()
        if not list_content.has_key('objects'):
            raise KeyError('Badly formatted reply')
        list_objects += list_content['objects']
        if autopage:
            while not list_content['meta']['next'] == None :
                list_request = re.get(self.root + list_content['meta']['next'], auth=self.auth)
                list_content = list_request.json()
                list_objects += list_content['objects']
        return list_objects

    def Get(self, resource='dataset', key='1'):
        """ Get an object identified by its key (id)

        :param resource: The type of object to get
        :param key: The unique identifier of the object

        Usage ::
        >>> import pymangal
        >>> mg = pymangal.mangal()
        >>> mg.Get('taxa', '1')
        """
        if isinstance(key, int):
            key = str(key)
        if not isinstance(key, str):
            raise TypeError("The key must be a string")
        if not isinstance(resource, str):
            raise TypeError("resource must be a string")
        if not resource in self.resources:
            raise ValueError("This type of resource is not available")
        get_url = self.url + resource + '/' + key
        get_request = re.get(get_url, auth=self.auth)
        if get_request.status_code == 404 :
            raise ValueError("There is no object with this identifier")
        if not get_request.status_code == 200 :
            raise ValueError("Request failed with status code "+str(get_request.status_code))
        return get_request.json()


