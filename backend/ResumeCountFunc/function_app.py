import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ResumeCountFunc")
@app.cosmos_db_input(
    arg_name="inputDocument",
    database_name="AzureResume",
    container_name="Counter",
    connection="AzureResumeConnectionString",
    sql_query="SELECT * FROM c WHERE c.id = '1'",
)
@app.cosmos_db_output(
    arg_name="outputDocument",
    database_name="AzureResume",
    container_name="Counter",
    connection="AzureResumeConnectionString",
    create_if_not_exists=False
)
def update_and_get_counter(req: func.HttpRequest, inputDocument: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Check if the document exists
    if not inputDocument:
        logging.error("Item with id '1' not found.")
        return func.HttpResponse(
            json.dumps({"error": "Item with id '1' not found."}),
            status_code=404,
            mimetype="application/json"
        )

    # Extract the 'counter' value
    document = inputDocument[0]  # Since we're querying by ID, we expect a single result
    counter_value = document.get("counter", None)

    if counter_value is None:
        logging.error("Field 'counter' not found in the item.")
        return func.HttpResponse(
            json.dumps({"error": "Field 'counter' not found in the item."}),
            status_code=400,
            mimetype="application/json"
        )

    # Increment the counter
    counter_value += 1
    document["counter"] = counter_value

    # Use the output binding to update the document in Cosmos DB
    outputDocument.set(func.Document.from_dict(document))

    # Return the updated counter value as JSON
    response_body = {
        "id": document["id"],
        "counter": counter_value
    }
    return func.HttpResponse(
        json.dumps(response_body),
        status_code=200,
        mimetype="application/json"
    )