'''
Main module for the NYPL Random Animal Generator.
'''
from flask import Flask, render_template

from lib.logger import Logger
from lib.nypldc_client import NyplDigitalCollectionClient
from lib.nypldc_exception import NyplBackendException

import json, sys

app = Flask(__name__)

nypl_client = None
logger = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/randimal/<animal>")
def random_animal(animal):
    try:
        animal_list = nypl_client.search_for_topic(animal)
    except NyplBackendException as e:
        logger.exception("Failed to get list of animal resouces.", e)
        return render_template("error.html")

    animal_list_count = len(animal_list)
    logger.info("Found {count} results for '{token}'".format(count=animal_list_count, token=animal))

    return render_template("random_animal.html", value=animal)

if __name__ == "__main__":
    logger = Logger()
    try:
        nypl_client = NyplDigitalCollectionClient()
    except FileNotFoundError:
        logger.error("Failed to find auth token- cannot start. See README for more info.")
        sys.exit(1)

    app.run()
