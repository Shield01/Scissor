import requests


def is_website_is_up(url: str):
    """
    The function checks if a website is up by sending a HEAD request and returning True if the status
    code is less than 500.

    :param url: A string representing the URL of a website that needs to be checked if it is up or not
    :type url: str
    :return: a boolean value (True or False) depending on whether the website at the given URL is up or
    not. If the response status code is less than 500, it returns True, indicating that the website is
    up. Otherwise, it returns False, indicating that the website is down.
    """
    response = requests.head(url)
    if response.status_code < 500:
        return True
    else:
        return False
