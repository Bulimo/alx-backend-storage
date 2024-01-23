#!/usr/bin/env python3
""" Module 102-log_stats """

from pymongo import MongoClient


def nginx_log_stats():
    """
    Module 12-log_stats
    script that provides some stats about Nginx logs stored in MongoDB
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx

    # Display the total number of logs
    print("{} logs".format(nginx_logs.count_documents({})))

    # Display methods statistics
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_logs.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    # Display status endpoint statistics
    status_count = nginx_logs.count_documents(
            {"method": "GET", "path": "/status"}
        )
    print("{} status check".format(status_count))

    ip_pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    ips = list(nginx_logs.aggregate(ip_pipeline))
    print("IPs:")
    for ip in ips:
        print("\t{}: {}".format(ip['_id'], ip['count']))


if __name__ == "__main__":
    nginx_log_stats()
