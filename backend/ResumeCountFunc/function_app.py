import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ResumeCountFunc")
@app.cosmos_db_input(
    arg_name="inputDocument",
    database_name="AzureResume",
    container_name="Counter",
    connection="AzureResumeConnectionString",
    sql_query="SELECT * FROM c WHERE c.id = '1'",
)
def get_counter(req: func.HttpRequest, inputDocument: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Check if the document exists
    if not inputDocument:
        logging.error("Item with id '1' not found.")
        return func.HttpResponse("Item with id '1' not found.", status_code=404)

    # Extract the 'counter' value
    document = inputDocument[0]  # Since we're querying by ID, we expect a single result
    counter_value = document.get("counter", None)

    if counter_value is None:
        logging.error("Field 'counter' not found in the item.")
        return func.HttpResponse("Field 'counter' not found in the item.", status_code=400)

    # Return the counter value
    return func.HttpResponse(f"The counter value is {counter_value}", status_code=200)