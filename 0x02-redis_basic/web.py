#!/usr/bin/env python3
"""
Module web that implements get_page function
"""
import requests
import redis
from functools import wraps
from typing import Callable

# Connect to Redis
redis_instance = redis.Redis()


def count_access(method: Callable) -> Callable:
    """
    Decorator to count the number of times a particular URL is accessed.
    """
    @wraps(method)
    def wrapper(url: str, *args, **kwargs):
        """ Count replacement function """
        key = f"count:{url}"
        redis_instance.incr(key)
        return method(url, *args, **kwargs)

    return wrapper


def cache_result(method: Callable) -> Callable:
    """
    Decorator to cache the result with an expiration time of 10 seconds.
    """
    @wraps(method)
    def wrapper(url: str, *args, **kwargs):
        """ Cache function """
        key = f"cache:{url}"
        result = redis_instance.get(key)

        if result is None:
            result = method(url, *args, **kwargs)
            redis_instance.setex(key, 10, result)

        return result

    return wrapper


@count_access
@cache_result
def get_page(url: str) -> str:
    """
    Gets the HTML content of a particular URL and caches the result.
    """
    response = requests.get(url)
    return response.text
