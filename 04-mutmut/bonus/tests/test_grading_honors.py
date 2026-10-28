import pytest

from grading_honors import is_honors


@pytest.mark.parametrize("scores", [[90], [90, 90], [100, 90], [95, 99, 91]])
def test_honors_true(scores):
    assert is_honors(scores) is True


@pytest.mark.parametrize("scores", [[89], [89.9], [90, 89], [0], [60, 80, 89]])
def test_honors_false(scores):
    assert is_honors(scores) is False


def test_honors_empty():
    with pytest.raises(ValueError, match=r"^scores must not be empty$"):
        is_honors([])
