import itertools
import random
from sample import sample


def test_sample_list():
    random.seed(44444)
    assert list(sample("abcdefghijklmnopqrstuvwxyz", 5)) == ["a", "e", "i", "j", "l"]


def test_sample_list_exhausted():
    # this test checks what happens if list is too short
    random.seed(11111)
    assert list(sample("abcdefghijklmnopqrstuvwxyz", 5)) == ["b", "f", "h", "z"]


def test_sample_list_rate_1():
    random.seed(44444)
    assert list(sample("abcdefghijklmnopqrstuvwxyz", 5, 1)) == ["a", "b", "c", "d", "e"]


def test_sample_list_rate_0():
    random.seed(44444)
    assert list(sample("abcdefghijklmnopqrstuvwxyz", 5, 0)) == []


def test_sample_list_sample_size_zero():
    random.seed(44444)
    assert list(sample("abcdefghijklmnopqrstuvwxyz", 0, 0)) == []


def test_random_seeded_infinite():
    random.seed(22222)
    # itertools.count counts up forever
    assert list(sample(itertools.count(), 4)) == [3, 16, 23, 36]
