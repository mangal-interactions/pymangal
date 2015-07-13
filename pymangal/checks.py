from jsonschema import validate

def check_resource_arg(api, resource):
    """Checks that the ``resource`` argument is correct

    :param api: A ``mangal`` instance
    :param resource: A user-supplied argument (tentatively, a string)

    :returns: Nothing, but fails if ``resource`` is not valid

    So as to be valid, a ``resource`` argument *must*

    * be of type ``str``
    * be included in ``api.resources``, which is collected from the API root

    """
    if not api.__class__.__name__ == 'mangal':
        raise TypeError("The API object must be an instance of the mangal class")
    if not isinstance(resource, str):
        raise TypeError("The resource argument must be given as a string")
    if not resource in api.resources:
        raise ValueError("The API do not expose resources of types "+resource)

def check_upload_res(api, resource, data):
    """Checks that the data to be uploaded are in the proper format

    :param api: A ``mangal`` instance
    :param resource: A resource argument
    :param data: The data to be uploaded. This is supposed to be a dict.

    :returns: Nothing, but fails if something is wrong.

    The first checks are basic:

    * the user must provide authentication
    * the data must be given as a dict

    The next check concers data validity, i.e. they must conform to the data schema
    in json, as obtained from the API root when calling ``__init__``.
    """
    # This saves a bunch of typing
    check_resource_arg(api, resource)
    # Next, checks on the data
    if not api.auth:
        raise ValueError("You need to provide authentication to post")
    if data == None :
        raise ValueError("You need to provide data")
    if not isinstance(data, dict):
        raise TypeError("Data must be in dict format")
    if not data.has_key('owner'):
        data['owner'] = api.owner
    # Remove fieds that are None
    for k, v in data.items():
        if v == None:
            data.pop(k, None)
    validate(data, api.schemes[resource])
    return data

def check_filters(filters):
    """Checks that the filters are valid

    :param filters: A string of filters

    :returns: Nothing, but can modify ``filters`` in place, and raises ``ValueError``s if the filters are badly formatted.

    This functions conducts minimal parsing, to make sure that the relationship exists, and that the filter is generally well formed.

    The ``filters`` string is modified in place if it contains space.
    """
    if not isinstance(filters, str):
        raise TypeError("filters must be a string")
    # We replace all spaces with %20
    filters.replace(' ', '%20')
    # These steps will check that the filters are correct
    REL = ['startswith', 'endswith', 'exact', 'contains', 'range', 'gt', 'lt', 'gte', 'lte', 'in']
    filters = filters.split('&')
    for fi in filters:
        if not '=' in fi:
            raise ValueError("Filter "+fi+" is invalid (no =)")
        if not '__' in fi:
            raise ValueError("Filter "+fi+" is invalid (no __)")
        splitted_filter = fi.split('=')
        match = splitted_filter[0]
        target = splitted_filter[1]
        request = match.split('__')
        relationship = request[len(request)-1]
        if not relationship in REL:
            raise ValueError("Filter "+fi+" is invalid ("+ relationship +" is not a valid relationship)")
    if len(filters) == 1 :
        return filters
    else :
        return '&'.join(filters)
