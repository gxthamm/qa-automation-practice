def get_grade(score):
    """Возвращает оценку (2-5) по 100-балльной шкале."""
    if score < 0 or score > 100:
        raise ValueError("score must be between 0 and 100")
    if score >= 90:
        return "5"
    if score >= 75:
        return "4"
    if score >= 60:
        return "3"
    return "2"


def is_passed(score, threshold=60):
    """Сдан ли предмет: балл не ниже порога."""
    return score >= threshold


def average(scores):
    """Средний балл группы."""
    if not scores:
        raise ValueError("scores must not be empty")
    return sum(scores) / len(scores)
