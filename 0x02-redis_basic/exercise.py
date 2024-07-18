#!/usr/bin/env python3
"""redis for python"""
from typing import Union, Callable, Any
import uuid
import redis
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """a system to count how many times methods Cache class are called"""
    @wraps(method)
    def check(self, *args, **kwargs) -> Any:
        """checks in the wrapper"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return check


def call_history(method: Callable) -> Callable:
    """tracks the call details of a method in the class"""
    @wraps(method)
    def check(self, *args, **kwargs) -> Any:
        """returns the method's output"""
        in_key = "{}:inputs".format(method.__qualname__)
        out_key = "{}:outputs".format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return check


def replay(fn: Callable) -> None:
    """displays the call history of the class' methods"""
    if fn is None or not hasattr(fn, "__self__"):
        return
    redis_store = getattr(fn.__self__, "_redis", None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = "{}:inputs".format(fxn_name)
    out_key = "{}:outputs".format(fxn_name)
    fxn_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_count = int(redis_store.get(fxn_name))
    print("{} was called {} times:".format(fxn_name, fxn_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print("{}(*{}) -> {}".format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    """Object to store redis data"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ a method to generate a random key"""
        key_generate = str(uuid.uuid4())
        self._redis.set(key_generate, data)
        return key_generate

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes]:
        """ a method to convert the data back to the desired redis format """
        catched = self._redis.get(key)
        return fn(catched) if fn is not None else catched

    def get_str(self, key: str) -> str:
        """a method that parametrize Cache.get with a string conversion ."""
        return self.get(key, lambda X: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """a method that parametrize Cache.get with the integer conversion."""
        return self.get(key, lambda x: int(x))
