import requests as re

# TODO Documentation -- docstrings

def uri_from_username(api, username):
    """Returns a URI from a username

    :param api: An API object
    :param username: The username for which you want the URI, as a string

    :returns: The URI as a string, and raises ``ValueError`` if there is no known user, ``TypeError`` if the arguments are not in the correct type.
    """
    # TODO CHECKS!!!
    if not type(username) in [str, unicode]:
        raise TypeError("The username should be given as a string.")
    user_url = api.url + 'user' + "?username__exact=" + username
    user_request = re.get(user_url, params=api.params)
    if user_request.status_code == 200 :
        user_objects = user_request.json()['objects']
        if len(user_objects) == 0 :
            raise ValueError("No user with this name")
        user_uri = api.suffix + 'user/' + str(user_objects[0]['id']) + '/'
        # FIXME else what?
        return user_uri

def prepare_data_for_patching(api, resource, data):
    original_owner =  data['owner']
    data["owner"] = uri_from_username(api, original_owner)
    return data

def check_data_from_api(api, resource, data):
    for k in data.keys():
        if api.schemes[resource]['properties'][k]['type'] == 'integer':
            if not data[k] == None:
                data[k] = int(data[k])
    return data

def keys_to_uri(api, resource, data):
    for k in [x for x in data.keys() if not x == 'owner']:
        if api.field_names.has_key(k):
            fname = api.field_names[k]
        else :
            fname = k
        if 'URI' in api.schemes[resource]['properties'][k]['description']:
            if api.schemes[resource]['properties'][k]['type'] == 'array':
                data[k] = map(lambda x: api.suffix + fname + '/' + x + '/', data[k])
            else :
                data[k] = api.suffix + fname + '/' + data[k] + '/'
    return data
