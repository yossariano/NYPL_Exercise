'''
Test cases for nypldc_client.py
'''

import pytest
from requests.structures import CaseInsensitiveDict
from unittest.mock import MagicMock

from nypldc_client import NyplDigitalCollectionClient
from nypldc_exception import NyplAuthException, NyplBackendException

# Constants
TMP_TOKEN_VALUE="abcd"
EXAMPLE_METADATA = """
{"uuid": "78315148-f068-8a8d-e040-e00a18064798",
"apiUri": "http://api.repo.nypl.org/api/v2/items/mods/78315148-f068-8a8d-e040-e00a18064798",
"title": "A meeting at Whipsnade.",
"typeOfResource": "still image",
"imageID": "1803585",
"itemLink": "http://digitalcollections.nypl.org/items/78315148-f068-8a8d-e040-e00a18064798",
"rightsStatement": "The copyright and related rights status of this item has been reviewed by The New York Public Library, but we were unable to make a conclusive determination as to the copyright status of the item. You are free to use this Item in any way that is permitted by the copyright and related rights legislation that applies to your use.",
"rightsStatementURI": "http://rightsstatements.org/vocab/UND/1.0/"}
"""

def test_get_token_invalid_path():

    # Use a path that has not been populated with a token
    client = NyplDigitalCollectionClient("invalid_path/invalid_token.txt")

    # Shoulda try to populate the token cache and fail
    with pytest.raises(NyplAuthException):
        client._get_token()

def test_get_token(tmp_path):

    client = _setup_client(tmp_path)

    # Should populate the token cache and succeed
    client._get_token()

    assert client.auth_token == TMP_TOKEN_VALUE

def test_make_request_failure(tmp_path):
    client = _setup_client(tmp_path)

    # Simulate getting an exception from the request
    client._execute_request = MagicMock(side_effect=RuntimeError("Server error"))

    with pytest.raises(NyplBackendException):
        client._make_request("someUrl")


def test_make_request_bad_status(tmp_path):
    client = _setup_client(tmp_path)

    # Simulate getting a bad status from the server
    client._execute_request = MagicMock(return_value=MockResponse(500))

    with pytest.raises(NyplBackendException):
        client._make_request("someUrl")

def test_make_request_success_empty(tmp_path):
    client = _setup_client(tmp_path)

    # Simulate doing a successful request with no results
    server_response = MockResponse(200)
    client._execute_request = MagicMock(return_value=server_response)

    response = client._make_request("someUrl")
    assert response == None

    expected_headers = CaseInsensitiveDict()
    expected_headers["Authorization"] = "Token token=\"{token}\"".format(token=TMP_TOKEN_VALUE)
    client._execute_request.assert_called_with("someUrl", headers=expected_headers)

def test_make_request_success(tmp_path):
    client = _setup_client(tmp_path)

    # Simulate doing a successful request
    server_response = MockResponse(200)

    server_response.set_content(EXAMPLE_METADATA)
    client._execute_request = MagicMock(return_value=server_response)

    response = client._make_request("someUrl")

    assert len(response) == 1

def test_topic_image_search(tmp_path):
    client = _setup_client(tmp_path)

    # Simulate doing a successful request
    server_response = MockResponse(200)
    server_response.set_content(EXAMPLE_METADATA)
    client._execute_request = MagicMock(return_value=server_response)

    response = client.topic_image_search("flamingos")

    assert len(response) == 1
    assert response[0].image_id == "1803585"
    assert response[0].item_link == "http://digitalcollections.nypl.org/items/78315148-f068-8a8d-e040-e00a18064798"

def _setup_client(tmp_path):
    tmp_token_path = tmp_path / "test_token.txt"
    with open(tmp_token_path, "w") as t:
        t.write(TMP_TOKEN_VALUE)

    return NyplDigitalCollectionClient(tmp_token_path)

class MockResponse:

    def __init__(self, status_code):
        self.content = "{}"
        self.status_code = status_code
        self.reason = ""

    def set_content(self, content):
        self.content = '{"nyplAPI":{"response":{"result":[' + content + ']}}}'
