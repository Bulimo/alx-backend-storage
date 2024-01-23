#!/usr/bin/env python3
""" Module 11-schools_by_topic """


def schools_by_topic(mongo_collection, topic):
    """
    returns the list of school having a specific topic

    Args:
        mongo_collection: pymongo collection object
        topic (string): topic searched

    Returns:
        list of schools
    """
    schools = list(mongo_collection.find({"topics": topic}))
    return schools


if __name__ == "__main__":
    pass
