#!/usr/bin/env python3
""" Module 101-students """


def top_students(mongo_collection):
    """
    Returns all students sorted by average score

    Args:
        mongo_collection: pymongo collection object

    Returns:
        Collection with averageScore key added
    """
    # Aggregation pipeline to calculate and sort by average score
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {"_id": "$_id", "name": {"$first": "$name"},
                    "totalScore": {"$sum": "$topics.score"}}},
        {"$project": {"_id": 1, "name": 1,
                      "averageScore": {"$avg": "$totalScore"}}},
        {"$sort": {"averageScore": -1}}
    ]

    # Execute the aggregation pipeline on the collection
    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students


if __name__ == "__main__":
    pass
