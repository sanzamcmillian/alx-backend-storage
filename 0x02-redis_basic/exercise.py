#!/usr/bin/env python3
"""_summary_"""
from typing import Union, Callable
import uuid
import redis


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ a method to generate a random key"""
        key_generate = str(uuid.uuid4())
        self._redis.set(key_generate, data)
        return key_generate

    def get(self, key: str, fn: Callable = None) -> Union[str, int, float, bytes]:
        """ a method to convert the data back to the desired redis format """
        catched = self._redis.get(key)
        return fn(catched) if fn is not None else catched

    def get_str(self, key: str) -> str:
        """a method that parametrize Cache.get with a string conversion ."""
        return self.get(key, lambda X: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """a method that parametrize Cache.get with the integer conversion."""
        return self.get(key, lambda x: int(x))
