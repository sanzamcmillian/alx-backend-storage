#!/usr/bin/env python3
""" inserts a new document in a collection based on kwargs """


def insert_school(mongo_collection, **kwargs):
    """ a function that inserts a new document in a collection based on kwargs."""
    res = mongo_collection.insert_one(kwargs)
    return res.inserted_id
