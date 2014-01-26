import json
from jsonschema import validate
import requests as re
from makeschema import makeschema
from checks import *

class mangal:
    """Creates an object of class ``mangal``

    This is the main class used by ``pymangal``. When called, it will return
    an object with all methods and attributes required to interact with
    the database.

    :param url: The URL of the site with the API (default: ``http://mangal.uqar.ca``)
    :param suffix: The suffix of the API (default: ``/api/v1/``)
    :param usr: Your username on the server (default: ``None``)
    :param pwd: Your password on the server (default: ``None``)

    :returns: An object of class ``mangal``

    """

    def __init__(self, url='http://mangal.uqar.ca', suffix='/api/v1/', usr=None, pwd=None):
        """Creates an instance of a ``mangal`` class

        """
        if not suffix[0] == '/':
            suffix = '/'+suffix
        if not suffix[-1:] == '/':
            suffix += '/'
        self.suffix = suffix
        auth = None
        self.owner = None
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
            url = url[:-1]
        # Now we create the URL property
        self.root = url
        self.url = self.root + self.suffix
        # We establish first contact with the API
        API = re.get(self.url, auth = auth)
        if not API.status_code == 200 :
            raise ValueError("The URL you provided ("+url+") gave a "+str(API.status_code)+" status code")
        self.resources = API.json().keys()
        # For each resource, we need to know which verbs are available
        self.schemes = {}
        allowed_verbs = {}
        for resource in self.resources:
            schema = self.root + API.json()[resource]['schema']
            schema_request = re.get(schema)
            if schema_request.status_code != 200 :
                raise ValueError("The schema for resource "+resource+" is not available")
            if not 'allowed_detail_http_methods' in schema_request.json():
                raise KeyError("The API do not give a list of allowed methods")
            allowed_verbs[resource] = schema_request.json()['allowed_detail_http_methods']
            self.schemes[resource] = makeschema(schema_request.json(), name=str(resource))
        self.verbs = allowed_verbs
        # We get the URI of the user
        if not self.auth == None :
            user_url = self.url + 'user' + "?username__exact=" + auth[0]
            user_request = re.get(user_url)
            if user_request.status_code == 200 :
                user_objects = user_request.json()['objects']
                if len(user_objects) == 0 :
                    raise ValueError("No user with this name")
                self.owner = self.suffix + 'user/' + str(user_objects[0]['id']) + '/'


    def List(self, resource='dataset', filters=None, page=10, offset=0):
        """ Lists all objects of a given resource type, according to a filter

        :param resource: The type of resource (default: ``dataset``)
        :param filters: A string giving the filtering criteria (default: ``None``)
        :param page: Either an integer giving the number of results to return, or ``'all'`` (default: ``10``)
        :param offset: Number of initial results to discard (default: ``0``)

        :returns: A ``dict`` with keys ``meta`` and ``objects``

        .. note::

            The ``objects`` key of the returned dictionary is a ``list`` of ``dict``, each being a record in the database. The ``meta`` key contains the ``next`` and ``previous`` urls, and the ``total_count`` number of objects for the request.
        
        """
        list_objects = []
        if isinstance(page, str):
            if not page == 'all':
                raise ValueError("If 'page' is given as a string, it must be 'all'")
        else :
            if isinstance(page, int):
                if page < 1 :
                    raise ValueError("page must be greater or equal to 1")
            else :
                raise TypeError("page must be either a string or an integer")
        if not isinstance(offset, int):
            raise TypeError("offset must be an integer")
        if offset < 0 :
            raise ValueError("offset must be positive")
        check_resource_arg(self, resource)
        if not filters == None:
            if not isinstance(filters, str):
                raise TypeError("filters must be a string")
        list_url = self.url + resource
        if page != 'all':
            off_pages = "limit="+str(page)+"&offset="+str(offset)
            if filters == None :
                filters = off_pages
            else :
                filters = off_pages + '&' + filters
        if not filters == None :
            list_url += '?' + filters
        list_request = re.get(list_url, auth=self.auth)
        if list_request.status_code != 200 :
            raise ValueError("There was an error in listing the objects. Status code "+str(list_request.status_code))
        list_content = list_request.json()
        if not list_content.has_key('objects'):
            raise KeyError('Badly formatted reply')
        list_objects += list_content['objects']
        if page == 'all':
            while not list_content['meta']['next'] == None :
                list_request = re.get(self.root + list_content['meta']['next'], auth=self.auth)
                list_content = list_request.json()
                list_objects += list_content['objects']
        return {'meta': list_content['meta'], 'objects': list_objects}

    def Get(self, resource='dataset', key='1'):
        """ Get an object identified by its key (id)

        :param resource: The type of object to get
        :param key: The unique identifier of the object
        :returns: A ``dict`` representation of the resource
    
        """
        if isinstance(key, int):
            key = str(key)
        if not isinstance(key, str):
            raise TypeError("The key must be a string")
        check_resource_arg(self, resource)
        get_url = self.url + resource + '/' + key
        get_request = re.get(get_url, auth=self.auth)
        if get_request.status_code == 404 :
            raise ValueError("There is no object with this identifier")
        if not get_request.status_code == 200 :
            raise ValueError("Request failed with status code "+str(get_request.status_code))
        return get_request.json()

    def Post(self, resource='taxa', data=None):
        """ Post a resource to the database

        :param resource: The type of object to post
        :param data: The dict representation of the object
        
        The ``data`` may or may not contain an ``owner`` key. If so, it
        must be the URI of the owner object. If no ``owner`` key is present,
        the value used will be ``self.owner``.

        .. note::
            
            This method converts the fields values to URIs automatically

        If the request is successful, this method will return the newly created
        object. If not, it will print the reply from the server and fail.

        """
        if self.auth == None :
            raise ValueError("You need to provide authentication to post")
        if data == None :
            raise ValueError("You need to provide data")
        if not isinstance(data, dict):
            raise TypeError("Data must be in dict format")
        check_resource_arg(self, resource)
        post_url = self.url + resource + '/'
        if not data.has_key('owner'):
            data['owner'] = self.owner
        ## We need to check that for each relation, the key is
        ## replaced by suffix + resource + key
        for k in [x for x in data.keys() if not x == 'owner']:
            if 'URI' in self.schemes[resource]['properties'][k]['description']:
                if self.schemes[resource]['properties'][k]['type'] == 'array':
                    data[k] = map(lambda x: self.suffix + k + '/' + x + '/', data[k])
                else :
                    data[k] = self.suffix + k + '/' + data[k] + '/'
        ## OK, moving on
        validate(data, self.schemes[resource])
        print data
        payload = json.dumps(data)
        post_request = re.post(post_url, auth=self.auth, data=payload, headers = {'content-type': 'application/json'})
        if post_request.status_code == 201 :
            return post_request.json()
        else :
            print post_request.json()
            raise ValueError("The request failed with status code "+str(post_request.status_code))
