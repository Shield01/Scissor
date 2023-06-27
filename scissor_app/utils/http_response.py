from fastapi import HTTPException


def raise_bad_request(message):
    """
    This function raises an HTTPException with a status code of 400 and a given error message.

    :param message: The message parameter is a string that represents the reason for the bad request. It
    will be included in the response sent back to the client to provide more information about the error
    """
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    """
    This function raises a 404 HTTP exception with a message indicating that the requested URL does not
    exist.

    :param request: The request parameter is an object that represents an HTTP request made to a web
    server. It contains information such as the URL of the request, the HTTP method used (e.g. GET,
    POST), headers, and any data sent in the request body
    """
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


def unauthorized_response(response):
    """
    This function raises an HTTPException with a status code of 401 and a given response message.

    :param response: The parameter "response" is a string that represents the reason for the
    unauthorized response. It will be used as the detail message in the HTTPException that will be
    raised
    """
    raise HTTPException(status_code=401, detail=response)
