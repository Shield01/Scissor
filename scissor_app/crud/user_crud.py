from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models import User
from ..schemas import user_schemas
from ..utils.auth import hashPassword
from .. utils import responses


def create_user_account(user: user_schemas.UserSignupSchema, db: Session):
    """
    This function creates a user account by hashing the password and adding the user's information to
    the database.

    :param user: A dictionary or object containing the user's signup information, such as their
    username, email address, and password
    :type user: user_schemas.UserSignupSchema
    :param db: The "db" parameter is a database session object that allows the function to interact with
    the database. It is likely an instance of a SQLAlchemy session object
    :type db: Session
    :return: either a successful operation response with the created user account as the data or a
    failed operation response with the error message.
    """
    try:

        hashedPassword = hashPassword(user.password)

        db_user = User(
            password=hashedPassword,
            username=user.username,
            email_address=user.email_address
        )

        db.add(db_user)

        db.commit()

        db.refresh(db_user)

        return responses.successful_operation_response(db_user)

    except Exception as error:
        print(error)
        return responses.failed_operation_response(error)


def find_user_by_email_or_username(user_id: str, db: Session):
    """
    This function searches for a user in a database by their email address or username and returns a
    success response with the user data if found, or a failed response if not found.

    :param user_id: a string representing either the email address or username of a user that we want to
    find in the database
    :type user_id: str
    :param db: The "db" parameter is a SQLAlchemy session object that is used to interact with the
    database. It allows the function to query the database and retrieve data
    :type db: Session
    :return: a response object, which could be either a successful operation response or a failed
    operation response. The response object contains data related to the operation performed in the
    function, such as the user data if the operation was successful, or an error message if the
    operation failed.
    """
    try:
        data = db.query(User).filter(
            or_(User.email_address == user_id, User.username == user_id)).first()

        if data:
            return responses.successful_operation_response(data)

        else:
            return responses.failed_operation_response(f"User with user id {user_id} does not exist")

    except Exception as e:
        return responses.failed_operation_response(e)
