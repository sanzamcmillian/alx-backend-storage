#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def nginx_logs(nginx_collection):
    """a function that prints stats about the nginx logs"""
    print("{} logs".format(nginx_collection.count_documents({})))
    print('Methods:')
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        req_count = len(list(nginx_collection.find({"method": method})))
        print("\tmethod {}: {}".format(method, req_count))
    status_check = len(list(
        nginx_collection.find({"method": 'GET', "path": "/status"})
    ))
    print("{} status check".format(status_check))


def run():
    """provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_logs(client.logs.nginx)


if __name__ == "__main__":
    run()
