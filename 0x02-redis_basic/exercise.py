#!/usr/bin/env python3
"""
Module exercise
Implements the class Cache
"""

import redis
from typing import Union, Callable, Optional
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Implements a decorator that takes argument
    returns a Callable
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Function that is implemented in the decorator """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    decorator to store the history of inputs and outputs
    for a particular function
    """
    key_inputs = method.__qualname__ + ":inputs"
    key_outputs = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ new function that will replace the original method """
        # Store input arguments
        self._redis.rpush(key_inputs, str(args))

        # Execute the wrapped function to get the output
        result = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(key_outputs, str(result))

        return result

    return wrapper


class Cache:
    """
    Defines the Cache class
    """

    def __init__(self) -> None:
        """ Defines the class __init__ method """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method that generate a random key, store the input data in Redis
        using the random key and return the key

        Args:
          data(Any): can be a str, bytes, int or float

        Returns:
          (string): randomly generated key
        """
        rand_key: str = str(uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[
            str, bytes, int, float, None]:
        """
        Implements custom get method
        """
        res: bytes = self._redis.get(key)

        if res is not None and fn is not None:
            return fn(res)
        return res

    def get_str(self, key: str) -> Optional[str]:
        """ Converts the returned value to str if possible """
        return self.get(
            key,
            fn=lambda d: d.decode("utf-8") if isinstance(d, bytes) else d
        )

    def get_int(self, key: str) -> Optional[int]:
        """ Converts the returned value to int if possible """
        return self.get(
            key,
            fn=lambda d: int(d) if d is not None else None
        )


def replay(method: Callable):
    """  function to display the history of calls of a particular function """
    cache: Cache = Cache()
    key_inputs = method.__qualname__ + ":inputs"
    key_outputs = method.__qualname__ + ":outputs"

    inputs = [
        input_args.decode('utf-8')
        for input_args in cache._redis.lrange(key_inputs, 0, -1)
    ]
    outputs = [
        output_result.decode(
            'utf-8') for output_result in cache._redis.lrange(
                key_outputs, 0, -1
        )
    ]

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_args, output_result in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_args}) -> {output_result}")
