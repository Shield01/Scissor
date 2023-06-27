import validators
from fastapi import APIRouter, Depends, Body, Header
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL as StarletteURL
from ..utils.http_response import raise_bad_request, unauthorized_response
from ..utils.graceful_forwarding import is_website_is_up
from ..utils.get_db import get_db
from ..utils.auth import authorize_request
from ..utils import responses
from ..utils.clean_objects import clean_object_for_output
from ..crud.url_crud import create_db_url, create_db_custom_shortened_url, delete_db_url, get_db_url_by_key, get_db_url_by_secret_key, peek_target_url_by_key, update_db_clicks, deactivate_db_url_by_secret_key
from ..schemas.url_schemas import URL, URLBase, URLInfo, CustomURLBase
from ..config import get_settings

url_router = APIRouter()

"""
    This function takes a database URL and returns a URLInfo object with the base URL, admin endpoint,
    and admin URL.

    :param db_url: The `db_url` parameter is an instance of the `URL` class, which contains information
    about a database URL, including the URL itself, a secret key, and an admin URL
    :type db_url: URL
    :return: a modified version of the input `db_url` object, which now includes an `admin_url`
    attribute that is a string representing the URL for accessing administration information related to
    the database. The `get_admin_info` function also modifies the `url` attribute of the `db_url` object
    to include the base URL. The returned object is of type `URLInfo`.
"""


def get_admin_info(db_url: URL) -> URLInfo:

    base_url = StarletteURL(get_settings().base_url)

    admin_endpoint = url_router.url_path_for(

        "administration info", secret_key=db_url.secret_key

    )
    db_url.url = str(base_url.replace(path=f"/url/{db_url.key}"))

    db_url.admin_url = str(base_url.replace(path=f"/url{admin_endpoint}"))

    return db_url


"""
    This function forwards a request to a target URL and updates the database with the number of clicks,
    but returns an error message if the target URL is not up.

    :param url_key: A string representing the unique key of the URL that needs to be forwarded to the
    target URL
    :type url_key: str
    :param db: The "db" parameter is a dependency injection that provides a database session to the
    function. It is used to interact with the database and perform CRUD operations. The "Session" type
    is imported from the SQLAlchemy package and represents a database session
    :type db: Session
    :return: a RedirectResponse object if the target URL is up and a failed_operation_response object if
    the target URL is not up or if the URL key is not found in the database.
"""


@url_router.get("/{url_key}")
async def forward_to_target_url(url_key: str, db: Session = Depends(get_db)):

    data = get_db_url_by_key(db=db, url_key=url_key)

    if data["status"] == "success":

        update_db_clicks(db=db, db_url=data["detail"])

        if is_website_is_up(data["detail"].target_url):

            return RedirectResponse(data["detail"].target_url)
        else:
            return responses.failed_operation_response("Target URL is not up")
    else:

        return data

"""
    This is an asynchronous Python function that retrieves a target URL by its key from a database using
    a helper function.

    :param url_key: The unique identifier/key for a specific URL in the database
    :type url_key: str
    :param db: The "db" parameter is a dependency injection that provides a database session to the
    function. It is used to interact with the database and perform CRUD (Create, Read, Update, Delete)
    operations. The "Session" type refers to a SQLAlchemy session object
    :type db: Session
    :return: The function `peek_target_url` is returning the result of calling the function
    `peek_target_url_by_key` with the arguments `db=db` and `url_key=url_key`. The result of this
    function call is a target URL or some linked to the url_key.
"""


@url_router.get("/peek/{url_key}")
async def peek_target_url(url_key: str, db: Session = Depends(get_db)):

    return peek_target_url_by_key(db=db, url_key=url_key)


"""
    This function retrieves admin information for a given secret key if the request is authorized.

    :param secret_key: A string representing the secret key of a URL that needs to be retrieved
    :type secret_key: str
    :param token: The token parameter is a header parameter that is used to authenticate the user making
    the request. It is optional and its default value is set to None
    :type token: str
    :param db: The parameter `db` is a dependency injection that provides a database session to the
    function `get_urls_admin_info()`. It is used to interact with the database and perform CRUD
    operations. The `get_db()` function is responsible for creating a new database session for each
    request and closing it after the request
    :type db: Session
    :return: either a successful operation response with the admin info obtained from the database, or
    an error response if the request is not authorized or if there is an error retrieving the data from
    the database.
"""


@url_router.get(
    "/admin/{secret_key}",
    name="administration info",
)
async def get_urls_admin_info(secret_key: str, token: str = Header(default=None), db: Session = Depends(get_db)):

    authorized_request = authorize_request(token)

    if authorized_request["status"] == "success":

        data = get_db_url_by_secret_key(db, secret_key=secret_key)

        if data["status"] == "success":

            del data["detail"].id

            return responses.successful_operation_response(get_admin_info(data["detail"]))

        else:

            return data
    else:
        raise unauthorized_response(
            "This resource is only available to authenticated users. Kindly login and try again")

"""
    This function retrieves the click statistics of a URL with a given secret key, after authorizing the
    request with a token.

    :param secret_key: A string representing the unique identifier for a URL in the database
    :type secret_key: str
    :param token: The token parameter is a header parameter that is used for authentication and
    authorization purposes. It is used to verify the identity of the user making the request and to
    ensure that they have the necessary permissions to access the requested resource
    :type token: str
    :param db: db is a parameter that represents a database session. It is obtained using the get_db
    function which is a dependency that is injected into the function using the Depends function from
    the FastAPI framework. The database session is used to query the database and retrieve the necessary
    data
    :type db: Session
    :return: a response object. If the request is authorized and the URL with the given secret key is
    found in the database, the function returns a successful operation response with the number of
    clicks for that URL. If the request is not authorized, an unauthorized response is raised. If the
    URL with the given secret key is not found in the database, the function returns the response
    specifying this result
"""


@url_router.get("/clicks_stats/{secret_key}")
async def get_url_click_stats(secret_key: str, token: str = Header(default=None), db: Session = Depends(get_db)):

    authorized_request = authorize_request(token)

    if authorized_request["status"] == "success":
        data = get_db_url_by_secret_key(db, secret_key=secret_key)
        if data["status"] == "success":
            return responses.successful_operation_response(data["detail"].clicks)
        else:
            return data
    else:
        raise unauthorized_response(
            "This resource is only available to authenticated users. Kindly login and try again")


"""
    This function shortens a given URL and returns a success response if the request is authorized and
    the URL is valid, otherwise it returns an error response.

    :param url: The URLBase object containing information about the URL to be shortened, including the
    target URL and any custom alias
    :type url: URLBase
    :param token: A string representing an authentication token that is used to authorize the request
    :type token: str
    :param db: The database session object used to interact with the database
    :type db: Session
    :return: a response object, either a successful operation response or an error response (bad request
    or unauthorized response).
"""


@url_router.post("/")
async def shorten_target_url(url: URLBase, token: str = Header(default=None), db: Session = Depends(get_db)):

    authorized_request = authorize_request(token)

    if authorized_request["status"] == "success":
        if not validators.url(url.target_url):
            raise_bad_request(message="Your provided target URL is not valid")

        data = create_db_url(db=db, url=url)

        if data["status"] == "success":

            mod = get_admin_info(data["detail"])

            mod = clean_object_for_output(mod)

            res = responses.successful_operation_response(mod)

            return res

        else:
            return data
    else:
        raise unauthorized_response(
            "This resource is only available to authenticated users. Kindly login and try again")


"""
    This function creates a custom shortened URL and returns a success response if the request is
    authorized and the URL is valid.

    :param url: The input parameter for the target URL that needs to be shortened and stored in the
    database
    :type url: CustomURLBase
    :param token: A string representing the authentication token for the user making the request. It is
    passed in the header of the HTTP request
    :type token: str
    :param db: The database session object used to interact with the database. It is obtained using the
    `get_db` dependency function
    :type db: Session
    :return: a response object, either a successful operation response or an error response, depending
    on the input parameters and the outcome of the function's operations. If the user is not authorized,
    an unauthorized response is raised.
"""


@url_router.post("/custom")
async def create_custom_shortened_url(url: CustomURLBase, token: str = Header(default=None), db: Session = Depends(get_db)):

    authorized_request = authorize_request(token)

    if authorized_request["status"] == "success":
        if not validators.url(url.target_url):
            raise_bad_request(message="Your provided target URL is not valid")

        data = create_db_custom_shortened_url(url=url, db=db)

        if data["status"] == "success":

            mod = get_admin_info(data["detail"])

            mod = clean_object_for_output(mod)

            res = responses.successful_operation_response(mod)

            return res
        else:
            return data
    else:
        raise unauthorized_response(
            "This resource is only available to authenticated users. Kindly login and try again")


"""
    This function deactivates a shortened URL in the database based on a secret key and returns a
    success response with the admin information or an error response.

    :param secret_key: A string representing the secret key of a shortened URL that needs to be disabled
    :type secret_key: str
    :param token: The token parameter is a string that represents an authorization token. It is passed
    as a header in the HTTP request
    :type token: str
    :param db: The database session object obtained from the get_db dependency. It is used to interact
    with the database and perform CRUD operations
    :type db: Session
    :return: a response object, either a successful operation response or an error response depending on
    the outcome of the function's logic.
"""


@url_router.put("/disable_url/{secret_key}")
async def disable_shortened_url(secret_key: str, token: str = Header(default=None), db: Session = Depends(get_db)):

    authorized_request = authorize_request(token)

    if authorized_request["status"] == "success":
        data = deactivate_db_url_by_secret_key(db, secret_key=secret_key)

        if data["status"] == "success":
            mod = get_admin_info(data["detail"])

            mod = clean_object_for_output(mod)

            res = responses.successful_operation_response(mod)

            return res
        else:
            return data
    else:
        raise unauthorized_response(
            "This resource is only available to authorized users. Kindly login and try again")


"""
    This function deletes a shortened URL from the database if the request is authorized.

    :param secret_key: The shortened URL's unique identifier or key that is used to retrieve and delete
    the URL from the database
    :type secret_key: str
    :param token: The token parameter is a string that represents an authentication token. It is passed
    in as a header in the HTTP request
    :type token: str
    :param db: The parameter `db` is a dependency injection that provides a database session to the
    function `delete_shortened_url()`. It is used to interact with the database and perform CRUD
    operations. The `get_db()` function is responsible for creating a new database session for each
    request and closing it after the request
    :type db: Session
    :return: a response object, either a successful operation response or an error response depending on
    the outcome of the function's logic.
"""


@url_router.delete("/delete_disabled_url/{secret_key}")
async def delete_shortened_url(secret_key: str, token: str = Header(default=None), db: Session = Depends(get_db)):

    authorized_request = authorize_request(token)

    if authorized_request["status"] == "success":
        data = delete_db_url(db, secret_key)

        if data["status"] == "success":

            return responses.successful_operation_response(data["detail"])

        else:
            return data
    else:
        raise unauthorized_response(
            "This resource is only available to authorized users. Kindly login and try again")
