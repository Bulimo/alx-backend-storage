#!/usr/bin/env python3
""" Module 9-insert_school """


def insert_school(mongo_collection, **kwargs):
    """
     Inserts a new document in a collection based on kwargs

     Args:
        mongo_collection: PyMongo collection object.
        **kwargs: fields and values of the document.

    Returns:
        The _id of the newly inserted document.
    """
    new_document = kwargs
    result = mongo_collection.insert_one(new_document)
    return result.inserted_id


if __name__ == "__main__":
    pass
