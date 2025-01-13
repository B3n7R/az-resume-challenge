import pytest
import azure.functions as func
import json
from unittest.mock import MagicMock
from ResumeCountFunc.function_app import main

class MockOutDocument:
    """Mock class to mimic the behavior of func.Out."""
    def __init__(self):
        self.value = None

    def set(self, document):
        self.value = document

@pytest.fixture
def mock_request():
    """Fixture to create a mock HTTP request."""
    return func.HttpRequest(
        method="GET",
        body=None,
        url="/api/update_and_get_counter"
    )

@pytest.fixture
def mock_document():
    """Fixture to create a mock Cosmos DB document."""
    return func.Document(
        {
            "id": "1",
            "counter": 4
        }
    )

def test_valid_increment(mock_request, mock_document):
    """Test case for a valid document with a counter field."""
    input_document = func.DocumentList([mock_document])
    output_document = MockOutDocument()

    # Call the function
    response = main(
        req=mock_request,
        inputDocument=input_document,
        outputDocument=output_document
    )

    # Validate the response
    assert response.status_code == 200
    response_body = json.loads(response.get_body())
    assert response_body["id"] == "1"
    assert response_body["counter"] == 5

    # Validate the output binding
    assert output_document.value is not None
    assert json.loads(output_document.value.to_json()) == {
        "id": "1",
        "counter": 5
    }

def test_missing_document(mock_request):
    """Test case when no document is found in the input."""
    input_document = func.DocumentList([])
    output_document = MockOutDocument()

    # Call the function
    response = main(
        req=mock_request,
        inputDocument=input_document,
        outputDocument=output_document
    )

    # Validate the response
    assert response.status_code == 404
    response_body = json.loads(response.get_body())
    assert response_body["error"] == "Item with id '1' not found."

def test_missing_counter_field(mock_request):
    """Test case when the 'counter' field is missing in the document."""
    
    mock_document = func.Document(
        {
            "id": "1"
        }
    )
    input_document = func.DocumentList([mock_document])
    output_document = MockOutDocument()

    # Call the function
    response = main(
        req=mock_request,
        inputDocument=input_document,
        outputDocument=output_document
    )

    # Validate the response
    assert response.status_code == 400
    response_body = json.loads(response.get_body())
    assert response_body["error"] == "Field 'counter' not found in the item."