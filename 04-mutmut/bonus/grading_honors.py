from grading import average


def is_honors(scores):
    """Отличник: средний балл не ниже 90."""
    return average(scores) >= 90
