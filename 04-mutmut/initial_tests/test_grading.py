import pytest

from grading import average, get_grade, is_passed


def test_grade_excellent():
    assert get_grade(95) == "5"


def test_grade_good():
    assert get_grade(80) == "4"


def test_grade_satisfactory():
    assert get_grade(70) == "3"


def test_grade_fail():
    assert get_grade(10) == "2"


def test_negative_score_is_invalid():
    with pytest.raises(ValueError):
        get_grade(-5)


def test_is_passed():
    assert is_passed(80)


def test_average():
    assert average([80, 90]) == 85


def test_average_empty():
    with pytest.raises(ValueError):
        average([])
