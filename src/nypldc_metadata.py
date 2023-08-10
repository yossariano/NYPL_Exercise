'''
Class which wraps NYPL Digital Collection metadata for images

Example image metadata:

    {'uuid': '78315148-f068-8a8d-e040-e00a18064798',
     'apiUri': 'http://api.repo.nypl.org/api/v2/items/mods/78315148-f068-8a8d-e040-e00a18064798',
     'title': 'A meeting at Whipsnade.',
     'typeOfResource': 'still image',
     'imageID': '1803585',
     'itemLink': 'http://digitalcollections.nypl.org/items/78315148-f068-8a8d-e040-e00a18064798',
     'rightsStatement': 'The copyright and related rights status of this item has been reviewed by The New York Public Library, but we were unable to make a conclusive determination as to the copyright status of the item. You are free to use this Item in any way that is permitted by the copyright and related rights legislation that applies to your use.',
     'rightsStatementURI': 'http://rightsstatements.org/vocab/UND/1.0/'}
'''

IMAGE_URL_FORMAT="https://images.nypl.org/index.php?id={image_id}&t=w"

# Metadata fields
METADATA_IMAGE_ID = "imageID"
METADATA_ITEM_LINK = "itemLink"

class NyplMetadata:

    def __init__(self, metadata):
        self.image_id = metadata.get(METADATA_IMAGE_ID)
        self.image_url = NyplMetadata.parse_image_url(metadata)
        self.item_link = metadata.get(METADATA_ITEM_LINK)

    @staticmethod
    def parse_image_url(image_metadata):
        image_id = image_metadata.get(METADATA_IMAGE_ID)
        return IMAGE_URL_FORMAT.format(image_id=image_id)
