from sqlalchemy.orm import Session
from ..utils import keygen, responses
from ..models import URL
from ..schemas import url_schemas


def create_db_url(db: Session, url: url_schemas.URLBase):
    """
    This function creates a new URL in the database with a unique key and secret key.

    :param db: The database session object used to interact with the database
    :type db: Session
    :param url: The `url` parameter is an instance of the `URLBase` class, which is a Pydantic model
    representing the data required to create a shortened URL. It contains a `target_url` field, which is
    the original URL that the user wants to shorten
    :type url: url_schemas.URLBase
    :return: either a successful operation response with the newly created URL object or a failed
    operation response with the error that occurred during the creation process.
    """
    try:
        key = keygen.create_unique_random_key(db)

        secret_key = f"{key}_{keygen.create_random_key(length=8)}"

        db_url = URL(
            target_url=url.target_url, key=key, secret_key=secret_key
        )

        db.add(db_url)

        db.commit()

        db.refresh(db_url)

        return responses.successful_operation_response(db_url)

    except Exception as error:
        return responses.failed_operation_response(error)


def create_db_custom_shortened_url(db: Session, url: url_schemas.CustomURLBase):
    """
    This function creates a shortened URL with a custom name and a randomly generated secret key in a
    database.

    :param db: The parameter `db` is an instance of the `Session` class, which is used to interact with
    the database. It is likely that this function is part of a larger application that uses an ORM
    (Object-Relational Mapping) framework such as SQLAlchemy to manage database operations. The
    `Session`
    :type db: Session
    :param url: The parameter `url` is an instance of the `CustomURLBase` schema, which contains
    information about a custom shortened URL that a user wants to create. It includes the target URL
    that the shortened URL should redirect to, as well as an optional custom name for the shortened URL
    :type url: url_schemas.CustomURLBase
    :return: either a successful operation response with the created URL object or a failed operation
    response with the error that occurred during the operation.
    """
    try:
        key = url.custom_name

        secret_key = f"{key}_{keygen.create_random_key(length=8)}"

        db_url = URL(
            target_url=url.target_url, key=key, secret_key=secret_key
        )

        db.add(db_url)

        db.commit()

        db.refresh(db_url)

        return responses.successful_operation_response(db_url)

    except Exception as error:
        return responses.failed_operation_response(error)


def get_db_url_by_key(db: Session, url_key: str):
    """
    This function retrieves a database URL by its key and returns a success or failure response.

    :param db: The parameter `db` is of type `Session`, which is likely an instance of a SQLAlchemy
    session used for database operations
    :type db: Session
    :param url_key: The url_key parameter is a string that represents the unique key associated with a
    shortened URL. This function retrieves the full URL associated with the given key from the database
    :type url_key: str
    :return: a response object, which could be either a successful operation response or a failed
    operation response. The response object contains information about the result of the operation, such
    as the data retrieved from the database or an error message.
    """
    try:
        data = db.query(URL).filter(URL.key == url_key,  URL.is_active).first()
        if data:

            return responses.successful_operation_response(data)

        else:

            return responses.failed_operation_response(f"Shortened URL with url key : {url_key} does not exist")
    except Exception as error:
        return responses.failed_operation_response(error)


def peek_target_url_by_key(db: Session, url_key: str):
    """
    The function retrieves the target URL associated with a given URL key from a database and returns a
    success or failure response depending on whether the URL is active or exists in the database.

    :param db: The parameter `db` is of type `Session`, which is an instance of a SQLAlchemy session. It
    is used to interact with the database and perform CRUD operations
    :type db: Session
    :param url_key: a string representing the key of a shortened URL in a database
    :type url_key: str
    :return: either a successful operation response with the target URL of a shortened URL if it exists
    and is active in the database, or a failed operation response with an appropriate error message if
    the shortened URL does not exist or is not active. If an exception occurs during the execution of
    the function, a failed operation response with the error message is returned.
    """
    try:
        if db_url := db.query(URL).filter(URL.key == url_key).first():

            if db_url.is_active:

                return responses.successful_operation_response(db_url.target_url)

            else:

                return responses.failed_operation_response(
                    "Shortened URL is not active")

        else:

            return responses.failed_operation_response("Shortened URL does not exist")

    except Exception as error:
        return responses.failed_operation_response(error)


def get_db_url_by_secret_key(db: Session, secret_key: str):
    """
    This function retrieves a database URL based on a given secret key and returns a success or failure
    response.

    :param db: The database session object used to query the database
    :type db: Session
    :param secret_key: A string representing the secret key of a shortened URL
    :type secret_key: str
    :return: a response object, which could be either a successful operation response or a failed
    operation response. The response object contains information about the result of the operation, such
    as the shortened URL data or an error message.
    """
    try:
        data = db.query(URL).filter(URL.secret_key == secret_key).first()

        if data:

            return responses.successful_operation_response(data)

        else:

            return responses.failed_operation_response(f"Shortened URL with secret key : {secret_key} does not exist")

    except Exception as error:
        return responses.failed_operation_response(error)


def update_db_clicks(db: Session, db_url: url_schemas.URL):
    """
    This function updates the number of clicks for a given URL in a database and returns a success or
    failure response.

    :param db: The parameter `db` is a SQLAlchemy session object that allows the code to interact with
    the database. It is used to execute database operations such as adding, updating, and deleting
    records
    :type db: Session
    :param db_url: The parameter `db_url` is an instance of the `URL` model/schema that represents a URL
    object in the database. It is used to update the number of clicks for that URL in the database
    :type db_url: url_schemas.URL
    :return: either a successful operation response with the updated URL object or a failed operation
    response with the error message.
    """

    try:
        db_url.clicks += 1

        db.commit()

        db.refresh(db_url)

        return responses.successful_operation_response(db_url)

    except Exception as error:
        return responses.failed_operation_response(error)


def deactivate_db_url_by_secret_key(db: Session, secret_key: str):
    """
    This function deactivates a database URL by its secret key.

    :param db: A database session object used to interact with the database
    :type db: Session
    :param secret_key: A string representing the secret key of a shortened URL in the database
    :type secret_key: str
    :return: either a successful operation response with the deactivated shortened URL detail or a
    failed operation response with an error message.
    """
    try:
        data = get_db_url_by_secret_key(db, secret_key)

        if data["status"] == "success":

            data["detail"].is_active = False

            db.commit()

            db.refresh(data["detail"])

            return responses.successful_operation_response(data["detail"])

        else:
            return responses.failed_operation_response(f"Shortened URL with secret key : {secret_key} does not exist")

    except Exception as error:
        return responses.failed_operation_response(error)
    

def activate_db_url_by_secret_key(db: Session, secret_key: str):
    """
    This function activates a shortened URL by setting its "is_active" attribute to True based on a
    given secret key.
    
    :param db: The database session object used to interact with the database
    :type db: Session
    :param secret_key: A string representing the secret key of a shortened URL
    :type secret_key: str
    :return: either a successful operation response or a failed operation response depending on the
    outcome of the try-except block.
    """
    try:
        data = get_db_url_by_secret_key(db, secret_key)

        if data["status"] == "success":

            data["detail"].is_active = True

            db.commit()

            db.refresh(data["detail"])

            return responses.successful_operation_response(data["detail"])

        else:
            return responses.failed_operation_response(f"Shortened URL with secret key : {secret_key} does not exist")
        
    except Exception as error:
        return responses.failed_operation_response(error)


def delete_db_url(db: Session, secret_key: str):
    """
    This function deletes a shortened URL from the database if it exists and is disabled.

    :param db: The database session object used to interact with the database
    :type db: Session
    :param secret_key: a string representing the unique identifier for a shortened URL in the database
    :type secret_key: str
    :return: a response object, either a successful operation response or a failed operation response,
    depending on the outcome of the try-except block.
    """
    try:
        data = get_db_url_by_secret_key(db, secret_key)
        if data["status"] == "success":
            if data["detail"].is_active == False:
                db.delete(data["detail"])

                db.commit()

                return responses.successful_operation_response("Shortened URL has been deleted")
            else:
                return responses.failed_operation_response("Shortened URL is not disabled")
        else:
            return responses.failed_operation_response(f"Shortened URL with secret key {secret_key} does not exist")

    except Exception as error:
        return responses.failed_operation_response(error)
