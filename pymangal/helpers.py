import requests as re

def uri_from_username(api, username):
    # TODO CHECKS!!!
    user_url = api.url + 'user' + "?username__exact=" + username
    user_request = re.get(user_url, params=api.params)
    if user_request.status_code == 200 :
        user_objects = user_request.json()['objects']
        if len(user_objects) == 0 :
            raise ValueError("No user with this name")
        user_uri = api.suffix + 'user/' + str(user_objects[0]['id']) + '/'
        return user_uri

def prepare_data_for_patching(api, resource, data):
    # Every field which is None is removed
    for k, v in data.items():
        if v == None:
            data.pop(k, None)
    # Transform the owner into its URI
    original_owner =  data['owner']
    data["owner"] = uri_from_username(api, original_owner)
    return data
