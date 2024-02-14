import json

def success_response(status_code, message, data=None):
    response_body = {"success": message}
    if data is not None:
        response_body["data"] = data

    return {
        "statusCode": status_code,
        "body": json.dumps(response_body,default=str)
    }


def error_response(status_code, message, data=None):
    response_body = {"error": message}
    if data is not None:
        response_body["data"] = data

    return {
        "statusCode": status_code,
        "body": json.dumps(response_body,default=str)
    }