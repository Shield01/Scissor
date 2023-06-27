from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Request
from ..utils.clean_objects import clean_user_object_for_output
from ..utils.get_db import get_db
from ..utils import responses
from ..utils.auth import check_password
from ..schemas.user_schemas import UserLoginSchema, UserSignupSchema
from ..crud.user_crud import create_user_account, find_user_by_email_or_username
user_router = APIRouter()


"""
    This function handles user sign up and returns a successful or failed operation response.

    :param user: The user parameter is an instance of the UserSignupSchema class, which is used to
    represent the data required to create a new user account. It contains fields such as
    username, email, password, and any other relevant user information
    :type user: UserSignupSchema
    :param db: The "db" parameter is a dependency injection that provides a database session to the
    function. It is used to interact with the database and perform CRUD (Create, Read, Update, Delete)
    operations. The "Session" type is imported from the SQLAlchemy library and represents a connection
    to the database. The
    :type db: Session
    :return: either a successful operation response or a failed operation response, depending on the
    result of the create_user_account function. If the result status is "success", a cleaned user object
    is returned as a successful operation response. If the result status is not "success", a failed
    operation response is returned with the detail of the result.
"""


@user_router.post("/sign_up")
def user_sign_up(user: UserSignupSchema, db: Session = Depends(get_db)):

    result = create_user_account(user, db)

    if result["status"] == "success":
        response = clean_user_object_for_output(result["detail"])

        return responses.successful_operation_response(response)
    else:
        return responses.failed_operation_response(result["detail"])


"""
    This function handles user login by checking the user's credentials and returning a response
    indicating whether the login was successful or not.

    :param user: The user parameter is of type UserLoginSchema, which is a Pydantic model representing
    the user's login credentials (user_id and password)
    :type user: UserLoginSchema
    :param db: The "db" parameter is a database session object that is obtained by calling the "get_db"
    function using the "Depends" dependency injection from the FastAPI framework. This session object is
    used to interact with the database and perform CRUD (Create, Read, Update, Delete) operations on the
    :type db: Session
    :return: either a successful operation response or a failed operation response, depending on whether
    the user's login credentials are correct or not. If there is an exception, it will also return a
    failed operation response.
"""


@user_router.post("/login")
def user_login(user: UserLoginSchema, db: Session = Depends(get_db)):

    try:
        db_user = find_user_by_email_or_username(user.user_id, db)

        is_password_correct = check_password(db_user["detail"], user.password)

        if is_password_correct["status"] == "success":

            return responses.successful_operation_response(is_password_correct["detail"])

        else:

            return is_password_correct

    except Exception as e:
        return responses.failed_operation_response(e)
