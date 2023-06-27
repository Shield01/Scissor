def successful_operation_response(data):
    """
    This function returns a dictionary with a "status" key set to "success" and a "detail" key set to
    the input data.

    :param data: The data parameter is a variable that contains the details of a successful operation.
    This could be any type of data, such as a string, integer, list, or dictionary. The function takes
    this data as input and returns a dictionary with two keys: "status" and "detail". The "status
    :return: A dictionary with two key-value pairs: "status" with the value "success" and "detail" with
    the value of the input parameter "data".
    """
    return {
        "status": "success",
        "detail": data
    }


def failed_operation_response(data):
    """
    The function returns a dictionary with a "failed" status and a detail message.

    :param data: The data parameter is a variable that contains information about the failed operation.
    This information could be an error message, a description of the problem, or any other relevant
    details that can help the user understand why the operation failed
    :return: A dictionary with two key-value pairs: "status" with the value "failed" and "detail" with
    the value of the input parameter "data".
    """
    return {
        "status": "failed",
        "detail": data
    }
