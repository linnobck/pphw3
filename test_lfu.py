import lfu


def test_lfu_cache_positional_args():
    @lfu.lfu_cache(10)
    def sum(a, b):
        sum._calls += 1
        return a + b

    sum._calls = 0

    assert sum(1, 2) == 3
    assert sum(1, 2) == 3
    assert sum._calls == 1


def test_lfu_cache_keyword_args():
    @lfu.lfu_cache(10)
    def sum(a, b):
        sum._calls += 1
        return a + b

    sum._calls = 0

    assert sum(a=1, b=2) == 3
    assert sum(a=1, b=2) == 3
    assert sum._calls == 1

    assert sum(a=2, b=1) == 3
    assert sum._calls == 2


def test_lfu_cache_combined_args():
    @lfu.lfu_cache(10)
    def sum(a, b, c, d):
        sum._calls += 1
        return a + b + c + d

    sum._calls = 0

    assert sum(1, 2, c=3, d=4) == 10
    assert sum(1, 2, c=3, d=4) == 10
    assert sum._calls == 1

    assert sum(1, 2, c=4, d=4) == 11
    assert sum._calls == 2

    assert sum(0, 2, c=4, d=4) == 10
    assert sum._calls == 3


def test_lfu_cache_complex_args():
    @lfu.lfu_cache(10)
    def f(*args, **kwargs):
        f._calls += 1
        return args, kwargs

    f._calls = 0

    assert f(1, 2, c=3, d=4) == ((1, 2), dict(c=3, d=4))
    assert f(1, 2, c=3, d=4) == ((1, 2), dict(c=3, d=4))
    assert f._calls == 1

    assert f(1, 2, c=0, d=4) == ((1, 2), dict(c=0, d=4))
    assert f._calls == 2


def test_lfu_cache_arg_types():
    @lfu.lfu_cache(10)
    def f(*args, **kwargs):
        f._calls += 1
        return args, kwargs

    f._calls = 0

    f(1)
    f(1)
    assert f._calls == 1
    f(1.0)
    f(1.0)
    assert f._calls == 2

    f(x=1)
    f(x=1)
    assert f._calls == 3
    f(x=1.0)
    f(x=1.0)
    assert f._calls == 4


def test_lfu_cache_expiry():
    @lfu.lfu_cache(7)
    def f(*args, **kwargs):
        f._calls += 1
        return args, kwargs

    f._calls = 0

    # populate cache: f(1) called once, f(2) called twice and so on...
    for x in range(1, 10):
        for _ in range(x):
            f(x)
    assert f._calls == 9

    # last 7 calls are in cache
    f(9)
    f(8)
    f(7)
    f(6)
    f(5)
    f(4)
    f(3)
    assert f._calls == 9

    # a new value, will remove element from cache
    f(2)
    assert f._calls == 10

    # element removed should have been 3 (LFU), so a call to 9 bumps call count
    f(3)
    assert f._calls == 11

    # cache should be 2,3,4,5,6,7,9 (8 popped)
    f(2)
    f(4)
    f(5)
    f(6)
    f(7)
    f(8)
    f(9)
    assert f._calls == 12


def test_cache_info_repr():
    ci = lfu.CacheInfo(max_size=99)
    assert repr(ci) == "CacheInfo(hits=0, misses=0, max_size=99, cur_size=0)"
    ci.hits = 3
    ci.misses = 10
    ci.cur_size = 11
    assert repr(ci) == "CacheInfo(hits=3, misses=10, max_size=99, cur_size=11)"


def test_cache_info_added_to_func_obj():
    @lfu.lfu_cache(5)
    def f(*args, **kwargs):
        return args, kwargs

    assert isinstance(f.cache_info, lfu.CacheInfo)


def test_lfu_no_parameters():
    @lfu.lfu_cache(5)
    def f():
        pass

    f()
    f()
    f()
    f()
    assert repr(f.cache_info) == "CacheInfo(hits=3, misses=1, max_size=5, cur_size=1)"


def test_cache_info_cur_size():
    @lfu.lfu_cache(5)
    def f(*args, **kwargs):
        return args, kwargs

    assert repr(f.cache_info) == "CacheInfo(hits=0, misses=0, max_size=5, cur_size=0)"

    f(1)
    f(2)
    f(3)
    assert repr(f.cache_info) == "CacheInfo(hits=0, misses=3, max_size=5, cur_size=3)"

    # not to exceed 5
    f(4)
    f(5)
    f(6)
    assert repr(f.cache_info) == "CacheInfo(hits=0, misses=6, max_size=5, cur_size=5)"


def test_cache_info_hits():
    @lfu.lfu_cache(5)
    def f(*args, **kwargs):
        return args, kwargs

    assert repr(f.cache_info) == "CacheInfo(hits=0, misses=0, max_size=5, cur_size=0)"

    f(1)
    f(2)
    f(3)
    f(1)
    assert repr(f.cache_info) == "CacheInfo(hits=1, misses=3, max_size=5, cur_size=3)"

    f(4)
    f(5)
    f(6)
    f(6)
    assert repr(f.cache_info) == "CacheInfo(hits=2, misses=6, max_size=5, cur_size=5)"


def test_cache_info_complex():
    @lfu.lfu_cache(7)
    def f(*args, **kwargs):
        return args, kwargs

    # populate cache: f(1) called once, f(2) called twice and so on...
    for x in range(1, 10):
        for _ in range(x):
            f(x)
    assert repr(f.cache_info) == "CacheInfo(hits=36, misses=9, max_size=7, cur_size=7)"

    # last 7 calls are in cache
    f(9)
    f(8)
    f(7)
    f(6)
    f(5)
    f(4)
    f(3)
    assert repr(f.cache_info) == "CacheInfo(hits=43, misses=9, max_size=7, cur_size=7)"

    # a new value, will remove element from cache
    f(2)
    assert repr(f.cache_info) == "CacheInfo(hits=43, misses=10, max_size=7, cur_size=7)"

    # element removed should have been 3 (LFU), so a call to 9 bumps call count
    f(3)
    assert repr(f.cache_info) == "CacheInfo(hits=43, misses=11, max_size=7, cur_size=7)"

    # cache should be 3,4,5,6,7,9
    f(3)
    f(4)
    f(5)
    f(6)
    f(7)
    f(8)
    f(9)
    assert repr(f.cache_info) == "CacheInfo(hits=50, misses=11, max_size=7, cur_size=7)"
