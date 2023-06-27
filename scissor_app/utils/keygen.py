import secrets
import string
from sqlalchemy.orm import Session
from ..crud import url_crud


def create_random_key(length: int = 5) -> str:
    """
    The function creates a random string of uppercase letters and digits with a specified length using
    the secrets module in Python.

    :param length: The length parameter is an integer that specifies the length of the random key that
    will be generated. By default, it is set to 5 if no value is provided when the function is called,
    defaults to 5
    :type length: int (optional)
    :return: a randomly generated string of length `length` (default value is 5) consisting of uppercase
    letters and digits.
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> str:
    """
    This function generates a unique random key for a database by checking if the key already exists in
    the database and generating a new one if necessary.

    :param db: Session object representing the database session
    :type db: Session
    :return: A randomly generated unique key that does not already exist in the database.
    """
    key = create_random_key()
    conditional_url = url_crud.get_db_url_by_key(db, key)
    while conditional_url["status"] == "success":
        key = create_random_key()
        conditional_url = url_crud.get_db_url_by_key(db, url_key=key)
    return key
