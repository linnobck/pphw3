import pytest
from scope_check import find_conflicts, clean_dict


@pytest.mark.parametrize(
    "old,new",
    [
        ({}, {}),
        ({"a": 1}, {"a": 1}),
        ({"a": 1, "_": 3}, {"a": 1}),
        ({"a": 1, "_": 3, "_a": 4}, {"a": 1}),
        ({"a": 1, "_": 3, "_a": 4, "b": 2}, {"a": 1, "b": 2}),
    ],
)
def test_clean_dict(old, new):
    assert clean_dict(old) == new


@pytest.mark.parametrize(
    "old,new",
    [
        ({}, {}),
        ({"a": 1}, {"a": 1}),
        ({"a": 1, "_": 3}, {"a": 1}),
        ({"a": 1, "_": 3, "_a": 4}, {"a": 1}),
        ({"a": 1, "_": 3, "_a": 4, "b": 2}, {"a": 1, "b": 2}),
    ],
)
def test_find_conflicts_cleans(old, new):
    assert find_conflicts(old)["locals"] == new


def test_find_conflicts_no_conflicts():
    assert find_conflicts({"a": 1})["conflicts"] == {}


def test_find_conflicts_with_conflicts():
    assert find_conflicts({"clean_dict": 1})["conflicts"] == {"clean_dict": clean_dict}
