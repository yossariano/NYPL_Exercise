'''
Main module for the NYPL Random Animal Generator.
'''
from flask import Flask, render_template

from nypldc_client import NyplDigitalCollectionClient
from nypldc_exception import NyplAuthException, NyplBackendException
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
    except (NyplAuthException, NyplBackendException) as e:
        app.logger.exception("Failed to get list of animal data from NYPL: {msg}".format(msg=repr(e)))
        return render_template("error.html")

    # Results inconsistently have image ids - filter out those that do not
    # TODO: Figure out why metadata sometimes doesn't have image_ids for the same item.
    animal_list = [animal for animal in animal_list if animal.image_id]
    animal_list_count = len(animal_list)

    if animal_list_count == 0:
        app.logger.error("Unable to find any results for {query}".format(query=animal))
        return render_template("404.html", value=animal)

    app.logger.info("Found {count} results for '{token}'".format(count=animal_list_count, token=animal))

    # Pick a random animal from the list to display
    random_animal_index = random.randint(0, animal_list_count - 1)
    random_animal = animal_list[random_animal_index]

    return render_template("random_animal.html",
            animal=animal,
            image_url=random_animal.image_url,
            item_url=random_animal.item_link)

if __name__ == "__main__":
    nypl_client = NyplDigitalCollectionClient()

    app.run()
