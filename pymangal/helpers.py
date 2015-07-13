import requests as re

# TODO Documentation -- docstrings

def uri_from_username(api, username):
    # TODO CHECKS!!!
    user_url = api.url + 'user' + "?username__exact=" + username
    user_request = re.get(user_url, params=api.params)
    if user_request.status_code == 200 :
        user_objects = user_request.json()['objects']
        if len(user_objects) == 0 :
            raise ValueError("No user with this name")
        user_uri = api.suffix + 'user/' + str(user_objects[0]['id']) + '/'
        # FIXME else what?
        return user_uri

def prepare_data_for_posting(api, resource, data):
    # Every field which is None is removed
    for k, v in data.items():
        if v == None:
            data.pop(k, None)
    return data

def prepare_data_for_patching(api, resource, data):
    # Transform the owner into its URI
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
