from logging import Logger
from requests import PreparedRequest, Response


def status_code_parse_helper(response: Response, logger: Logger):
    if response.status_code != 200:
        logger.log(3, "Error Occurred while making the request.")
        logger.log(3, f"Response Code: {response.status_code}")
        if response.status_code == 401:
            logger.log(2, "Cannot complete the request.")
            logger.log(2, f"Error Message Received: {response.content}")
            if "errors" in response:
                logger.log(3, f"ErrorCode: {response["errors"]["code"]}")
    else:
        logger.log(1, f"Request success. Request status_code: {response.status_code}")
        logger.log(1, f"Request success. Request status_code: {response}")

def print_request_object_helper(requestObj: PreparedRequest):
    # Printing out the details of a prepared
    print(f"{requestObj.method} {requestObj.url}\n")
    for key, value in requestObj.headers.items():
        print(f"{key}: {value}")
    
    if requestObj.body:
        print(requestObj.body)

