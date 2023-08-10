'''
Test cases for nypldc_client.py
'''

import json, pytest
from flask import Flask
from unittest.mock import MagicMock

from nypldc_exception import NyplBackendException
from nypldc_metadata import NyplMetadata

import app

# Constants
EXAMPLE_METADATA_WITH_IMAGE = json.loads("""
{"title": "Cats and Dogs.",
"typeOfResource": "still image",
"imageID": "12345",
"itemLink": "itemLink1"}
""")

EXAMPLE_METADATA_WITHOUT_IMAGE = json.loads("""
{"title": "Baby Geniuses.",
"typeOfResource": "still image",
"itemLink": "itemLink2"}
""")


# Flask needs an app context while running these tests
@pytest.fixture(autouse=True)
def app_context():
    flask = Flask(__name__)
    with flask.app_context():
        yield

def test_random_animal_failure(app_context):
    app.nypl_client = MagicMock()
    app.nypl_client.topic_image_search = MagicMock(side_effect=NyplBackendException("Something went wrong.."))
    app.render_template = MagicMock()

    response = app.random_animal("dog")

    app.render_template.assert_called_with("error.html")

def test_random_animal_empty(app_context):
    app.nypl_client = MagicMock()
    app.nypl_client.topic_image_search = MagicMock(return_value=[])
    app.render_template = MagicMock()

    response = app.random_animal("pigs_flying")

    app.render_template.assert_called_with("404.html", value="pigs_flying")

def test_random_animal_missing_image(app_context):
    app.nypl_client = MagicMock()

    # Metadata without an image id will be filtered out
    app.nypl_client.topic_image_search = MagicMock(return_value=[NyplMetadata(EXAMPLE_METADATA_WITHOUT_IMAGE)])
    app.render_template = MagicMock()

    response = app.random_animal("invisible_goat")

    app.render_template.assert_called_with("404.html", value="invisible_goat")

def test_random_animal_success(app_context):
    app.nypl_client = MagicMock()
    app.nypl_client.topic_image_search = MagicMock(return_value=[NyplMetadata(EXAMPLE_METADATA_WITH_IMAGE)])
    app.render_template = MagicMock()

    response = app.random_animal("cat")

    app.render_template.assert_called_with("random_animal.html",
            animal="cat",
            image_url='https://images.nypl.org/index.php?id=12345&t=w',
            item_url="itemLink1")
