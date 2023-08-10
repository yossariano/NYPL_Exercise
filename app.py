'''
Main module for the NYPL Random Animal Generator.
'''
from flask import Flask, render_template

from nypldc_client import NyplDigitalCollectionClient
from nypldc_exception import NyplBackendException
from nypldc_metadata import NyplMetadata

import random, sys

app = Flask(__name__)

nypl_client = None

@app.route("/")
def index():
    return render_template("index.html")

# Example URL invocation:
# http://127.0.0.1:5000/randimal/flamingo
@app.route("/randimal/<animal>")
def random_animal(animal):
    try:
        animal_list = nypl_client.topic_image_search(animal)
    except NyplBackendException as e:
        app.logger.error("Failed to get list of animal data from NYPL.")
        return render_template("error.html")

    if not animal_list or len(animal_list) == 0:
        app.logger.error("Unable to find any results for {query}".format(query=animal))
        return render_template("404.html", value=animal)

    animal_list_count = len(animal_list)
    app.logger.info("Found {count} results for '{token}'".format(count=animal_list_count, token=animal))

    # Pick a random animal from the list to display
    random_animal_index = random.randint(0, animal_list_count - 1)
    random_animal = animal_list[random_animal_index]

    if not random_animal.image_id:
        # Some of the entries don't have an image in them.
        # If this is the case, just tell people to try again
        return render_template("retry.html",
                animal=animal,
                item_url=random_animal.item_link)

    return render_template("random_animal.html",
            animal=animal,
            image_url=random_animal.image_url,
            item_url=random_animal.item_link)

if __name__ == "__main__":
    try:
        nypl_client = NyplDigitalCollectionClient()
    except FileNotFoundError:
        app.logger.error("Failed to find auth token- cannot start. See README for more info.")
        sys.exit(1)

    app.run()
