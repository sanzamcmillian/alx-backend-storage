#!/usr/bin/env pyhton3
"""Implementing an expiring web cache and tracker"""
import requests
import redis
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def cacher(method: Callable) -> Callable:
    """caches the data """
    @wraps(method)
    def wrapper(url: str) -> str:
        """wrapper method"""
        redis_store.incr(f"count:{url}")
        result = redis_store.get(f"html:{url}")
        if result is not None:
            return result.decode("utf-8")
        result = method(url)
        redis_store.setex(f"html:{url}", 10, result)
        return result
    return wrapper


@cacher
def get_page(url: str) -> str:
    """requests module to obtain the HTML content of a URL"""
    response = requests.get(url)
    return response.text
