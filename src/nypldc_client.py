'''
Class which handles authentication and requests to the NYPL backend.

See http://api.repo.nypl.org/ for API details.

Requires a NYPL auth token available to the server at nypl_token.txt
'''
import json, requests
from nypldc_exception import NyplBackendException
from nypldc_metadata import NyplMetadata
from requests.structures import CaseInsensitiveDict

# Constants
BASE_URL="http://api.repo.nypl.org/api/v2/"
DEFAULT_TOKEN_PATH="nypl_token.txt"
# For parsing responses in a standardized way
RESPONSE_FIELD_API="nyplAPI"
RESPONSE_FIELD="response"
RESULT_FIELD="result"

# Status code handling
STATUS_OK=200

class NyplDigitalCollectionClient:

    def __init__(self, token_path=DEFAULT_TOKEN_PATH):
        self.auth_token = ""
        self.auth_token_path = token_path

    # Given a subject, returns a list of NyplMetadata objects for images making the search term.
    #
    # See:
    # http://api.repo.nypl.org/#items-search
    #
    # TODO: Handle pagination. For demonstration purposes, this app will not pull more than the first page of results
    def topic_image_search(self, topic):

        request_url = "{base_url}/items/search?field=topic&ftype=still+image&q={topic}".format(base_url=BASE_URL, topic=topic)

        # This should return a list
        response = self._make_request(request_url)

        if not response:
            return []

        # Return parsed metadata values
        return [NyplMetadata(item) for item in response]

    # Fetch the cached token if it is available, or else try to read it from disk
    def _get_token(self):
        if not self.auth_token:
            with open(self.auth_token_path) as t:
                self.auth_token = t.read().strip()
        return self.auth_token

    # Use the auth token and provided URL to call the NYPL backend
    def _make_request(self, url):

        headers = CaseInsensitiveDict()
        headers["Authorization"] = "Token token=\"{token}\"".format(token=self._get_token())

        response = None
        try:
            response = self._execute_request(url, headers=headers)
        except RuntimeError as e:
            raise NyplBackendException("Failure when attempting to call NYPL backend.", e)

        if response.status_code != STATUS_OK:
            raise NyplBackendException("Got error from NYPL backend: {error}".format(error=response.reason))

        # Pull the content out of the response:
        return json.loads(response.content).get(RESPONSE_FIELD_API, {}).get(RESPONSE_FIELD, {}).get(RESULT_FIELD)

    # Isolate for ease of mocking
    def _execute_request(self, url, headers=[]):
        return requests.get(url, headers=headers)
