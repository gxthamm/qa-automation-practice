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


# --- усиление тестов после разбора выживших мутантов ---


@pytest.mark.parametrize(
    "score, expected",
    [
        (0, "2"),
        (59, "2"),
        (60, "3"),
        (74, "3"),
        (75, "4"),
        (89, "4"),
        (90, "5"),
        (100, "5"),
    ],
)
def test_grade_boundaries(score, expected):
    assert get_grade(score) == expected


@pytest.mark.parametrize("score", [-1, -100, 101, 1000])
def test_score_out_of_range_is_invalid(score):
    # якоря ^ и $ не дают мутанту с «XX...XX» пережить проверку текста
    with pytest.raises(ValueError, match=r"^score must be between 0 and 100$"):
        get_grade(score)


def test_is_passed_uses_default_threshold():
    assert is_passed(60) is True
    assert is_passed(59) is False


def test_is_passed_with_explicit_threshold():
    assert is_passed(70, 70) is True
    assert is_passed(69, 70) is False


def test_average_returns_fractional_value():
    # нецелый результат ловит подмену деления на целочисленное
    assert average([80, 91]) == 85.5


def test_average_empty_message():
    with pytest.raises(ValueError, match=r"^scores must not be empty$"):
        average([])
