#!/usr/bin/env python3
"""_summary_"""
from typing import Union
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
