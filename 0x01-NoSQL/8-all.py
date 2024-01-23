#!/usr/bin/env python3
""" Module 8-all """


def list_all(mongo_collection):
    """
    Function that lists all documents in a collection.

    Args:
        mongo_collection: PyMongo collection object.

    Returns:
        A list of documents in the collection or empty list.
    """
    documents = list(mongo_collection.find({}))
    return documents


if __name__ == "__main__":
    pass
