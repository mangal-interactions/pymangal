# functions to check user-supplied arguments

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
