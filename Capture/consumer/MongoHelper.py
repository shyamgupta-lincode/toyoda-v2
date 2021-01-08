from pymongo import MongoClient


class mongo_client():
    """
    Creates a mongo client for accessing and performing operations on a mongo database that is hosted on a mongo server
    """

    def __init__(self, mongo_host, mongo_port):
        """
        Instantiates a pymongo client fir interacting with the mongo database

        Arguments:
            mongo_host: host for connecting to the server hosting the mongo server
            mongo_port: port for connecting to the server hosting the mongo server
        """
        self.client = MongoClient(mongo_host, int(mongo_port))

    def add_to_metadata_collection(self, part_name, topic):
        """"
        Registers the part id/name to the "parts metadata" collection

        Arguments:
            part_name: part to be registered
            topic: topic that the consumer receives the images for the given part

        """
        db = self.client["parts-metadata"]
        metadata_table = db.partsmetadata
        metadata_table.insert_one({"part_name": part_name, "topic": topic})
        part_payload = metadata_table.find_one({"topic": topic})
        part_id = part_payload["_id"]
        return part_id

    def add_to_parts_collection(self, payload):
        """
        Records the image data received for the given topic

        Arguments:
            payload: Collection to be added to the "parts collection"
        """
        db = self.client["parts-collection"]
        parts_table = db.parts
        parts_table.insert_one(payload)
        return

