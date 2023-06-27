import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from ..config import get_settings
from ..utils import responses


JWT_SECRET = get_settings().jwt_secret
JWT_ALGORITHM = get_settings().jwt_algorithm
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashPassword(password: str):
    """
    This function takes a password string as input and returns its hashed value using a password
    context.

    :param password: The parameter "password" is a string that represents the password that needs to be
    hashed
    :type password: str
    :return: the hashed version of the input password string using a password hashing algorithm
    specified by the `password_context` object.
    """
    return password_context.hash(password)


def check_password(user_data, password):
    """
    This function checks if a given password matches the user's password, and if so, generates a JWT
    token.

    :param user_data: This parameter is likely an object or dictionary containing information about the
    user, such as their ID and password hash
    :param password: The password input that needs to be checked against the user's stored password
    :return: a response based on the input parameters. The response could be a successful operation
    response with a token, a failed operation response with an error message, or a failed operation
    response with a message indicating that the password input is incorrect.
    """
    try:
        verify_password = password_context.verify(password, user_data.password)

        if verify_password:

            token = sign_jwt(user_data.id)

            if token["status"] == "success":

                return responses.successful_operation_response(token["detail"])

            else:

                return responses.failed_operation_response(token["detail"])
        else:

            return responses.failed_operation_response("Incorrect password inputed")

    except Exception as error:

        return responses.failed_operation_response(error)


def sign_jwt(user_id):
    """
    This function generates a JSON Web Token (JWT) containing a user ID and expiration time.

    :param user_id: The user ID is a unique identifier for a user in the system. It is used to associate
    the JWT token with a specific user
    :return: a response object. If the operation is successful, it returns a response object with a JWT
    token. If the operation fails, it returns a response object with an error message.
    """
    try:
        payload = {
            "user_id": user_id,
            "expires": (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S.%f"),
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return responses.successful_operation_response(token)

    except Exception as e:

        return responses.failed_operation_response(e)


def decode_token(token):
    """
    This function decodes a JWT token and checks if it is valid and not expired.

    :param token: This is a string representing the JWT token that needs to be decoded
    :return: either a successful operation response with the decoded token if the token is valid and has
    not expired, or a failed operation response with an appropriate error message if the token is
    invalid or has expired.
    """
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    if decoded_token:

        expiry_time = datetime.strptime(

            decoded_token['expires'], "%Y-%m-%d %H:%M:%S.%f")

        if expiry_time >= datetime.now():

            return responses.successful_operation_response(decoded_token)

        else:
            return responses.failed_operation_response("Provided token has expired")

    else:
        return responses.failed_operation_response("Provided token is invalid")


def verify_token(token: str):
    """
    The function verifies if a token is valid by decoding it and checking its payload status.

    :param token: a string representing a token that needs to be verified
    :type token: str
    :return: a response object that indicates whether the token is valid or not. If the token is valid,
    it returns a successful operation response with a boolean value of True. If the token is not valid,
    it returns a failed operation response with a boolean value of False.
    """
    is_token_valid: bool = False

    payload = decode_token(token)

    if payload["status"] == "success":

        is_token_valid = True

        return responses.successful_operation_response(is_token_valid)

    else:
        return responses.failed_operation_response(is_token_valid)


def authorize_request(token: str):
    """
    This function authorizes a request by verifying a token and returning a success or failure response.

    :param token: a string representing an authentication token that needs to be verified
    :type token: str
    :return: either a successful operation response with a boolean value of True if the token is valid,
    or a failed operation response with an error message if the token is invalid or if an exception
    occurs during the verification process.
    """
    try:
        request_is_valid = verify_token(token)

        if request_is_valid["status"] == "success":

            return responses.successful_operation_response(True)

        else:

            return responses.failed_operation_response("This resource is only available to authenticated users. Kindly login and try again")

    except Exception as e:

        return responses.failed_operation_response(e)
