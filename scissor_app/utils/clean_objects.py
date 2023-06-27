def clean_object_for_output(obj):
    """
    The function removes sensitive information from an object before outputting it.

    :param obj: The parameter "obj" is an object that is being passed to the function
    "clean_object_for_output". The function removes the "id", "key", and "secret_key" attributes from
    the object and returns the modified object
    :return: the `obj` after removing the `id`, `key`, and `secret_key` attributes if they exist in the
    object.
    """
    if obj.id:
        del obj.id

    if obj.key:
        del obj.key

    if obj.secret_key:
        del obj.secret_key

    return obj


def clean_user_object_for_output(obj):
    """
    The function removes the 'id' and 'password' attributes from a given object and returns the modified
    object.

    :param obj: The parameter "obj" is likely an object or instance of a user class that contains
    various attributes such as id, username, email, password, etc. The function
    "clean_user_object_for_output" takes this object as input and removes the "id" and "password"
    attributes from it before returning
    :return: the `obj` after deleting its `id` and `password` attributes.
    """
    del obj.id
    del obj.password
    return obj
