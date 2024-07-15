#!/usr/bin/env python3
"""list of all documents in a collection"""


def list_all(mongo_collection):
    """function that lists all documents in a collection"""
    return [doc for doc in mongo_collection.find()]
