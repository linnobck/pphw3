import random


class CacheInfo:
    """
    CacheInfo object used to represent the current status of `lfu_cache`
    """

    def __init__(self, max_size):
        self.max_size = max_size
        self.misses = 0  # Number of calls to the function where the result needed to be calculated by calling the function.
        self.hits = 0  # Number of calls to the function where the result was returned from the cache.
        self.cur_size = 0  # The number of entries currently stored.

    def __repr__(self):
        return f"CacheInfo(hits={self.hits}, misses={self.misses}, max_size={self.max_size}, cur_size={self.cur_size})"


# helper function for in cache logic
def key_in_cache(key, cache, count, info):
    info.hits += 1
    count[key] += 1

    return cache[key]


# helper function for deleting lfu item logic
def kick_out_lfu(cache, count, info):
    # prevent index error
    if not count:
        return

    min_calls = min(count.values())

    # get all keys that match the lowest count
    # for when multiple lfu
    lfu_keys = []
    for key, calls in count.items():
        if calls == min_calls:
            lfu_keys.append(key)

    # randomly select key to delete
    if lfu_keys:
        key_to_delete = random.choice(lfu_keys)

        del cache[key_to_delete]
        del count[key_to_delete]

    info.cur_size -= 1


# helper function for not in cache logic
def key_not_in_cache(key, func, args, kwargs, cache, count, info):
    if info.cur_size >= info.max_size:
        kick_out_lfu(cache, count, info)
        print("deleting from cache, adding to cach")

    result = func(*args, **kwargs)
    cache[key] = result
    info.misses += 1
    info.cur_size += 1
    count[key] = 1

    return result


# outer factory
def lfu_cache(max_size):
    # actual decorator that receives the function to wrap
    def cache_decorator(func):
        info = CacheInfo(max_size)
        cache = {}
        count = {}

        # inner function that runs every time we call the decorated function
        def new_func(*args, **kwargs):
            # arguments stay distinct, for same value ints and floats
            distinct_args = tuple((type(i), i) for i in args)
            distinct_kwargs = frozenset((k, (type(v), v)) for k, v in kwargs.items())

            key = (distinct_args, distinct_kwargs)

            # check if tuple is in cache
            if key not in cache:
                print("adding to cache")
                return key_not_in_cache(key, func, args, kwargs, cache, count, info)
            else:
                print("getting from cache")
                return key_in_cache(key, cache, count, info)

        new_func.cache_info = info
        return new_func

    return cache_decorator
