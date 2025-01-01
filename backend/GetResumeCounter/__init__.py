import logging

import azure.functions as func

from .get_resume_counter import get_counter


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    response = get_counter(req)
    if response is None:
        return func.HttpResponse("Unexpected error occurred.", status_code=500)
    return response
