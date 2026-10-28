import sqlite3


def get_balance(conn, name):
    """Возвращает остаток по счёту."""
    row = conn.execute("SELECT balance FROM accounts WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise ValueError(f"unknown account: {name}")
    return row[0]


def transfer(conn, source, target, amount):
    """Переводит amount со счёта source на счёт target в одной транзакции."""
    if amount <= 0:
        raise ValueError("amount must be positive")
    with conn:  # COMMIT при успехе, ROLLBACK при исключении
        balance = get_balance(conn, source)
        if balance < amount:
            raise ValueError("insufficient funds")
        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE name = ?",
            (amount, source),
        )
        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE name = ?",
            (amount, target),
        )


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE accounts (name TEXT PRIMARY KEY, balance INTEGER)")
    conn.executemany(
        "INSERT INTO accounts VALUES (?, ?)",
        [("Текущий счёт", 10000), ("Накопительный счёт", 0)],
    )
    transfer(conn, "Текущий счёт", "Накопительный счёт", 500)
    assert get_balance(conn, "Текущий счёт") == 9500
    assert get_balance(conn, "Накопительный счёт") == 500
    try:
        transfer(conn, "Текущий счёт", "Накопительный счёт", 20000)
        raise AssertionError("Ожидалась ошибка")
    except ValueError:
        pass
    assert get_balance(conn, "Текущий счёт") == 9500  # откат транзакции
    print("OK")
