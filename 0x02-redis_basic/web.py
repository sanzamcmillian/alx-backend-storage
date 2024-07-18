#!/usr/bin/env pyhton3
"""Implementing an expiring web cache and tracker"""
import requests
import redis
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""redis instance"""


def cacher(method: Callable) -> Callable:
    """caches the data """
    @wraps(method)
    def invoke(url) -> str:
        """wrapper method"""
        redis_store.incr(f"count:{url}")
        result = redis_store.get(f"result:{url}")
        if result:
            return result.decode("utf-8")
        result = method(url)
        redis_store.set(f"count:{url}", 0)
        redis_store.setex(f"result:{url}", 10, result)
        return result
    return invoke


@cacher
def get_page(url: str) -> str:
    """requests module to obtain the HTML content of a URL"""
    return requests.get(url).text
