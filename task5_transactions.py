import sqlite3


def main():
    """Демонстрация работы транзакций в SQLite."""
    conn = sqlite3.connect('transactions.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            name TEXT,
            balance REAL
        )
    ''')
    conn.commit()

    # Очистка
    cur.execute('DELETE FROM accounts')
    cur.execute(
        'INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)',
        (1, 'Ани', 1000.0)
    )
    cur.execute(
        'INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)',
        (2, 'Иван', 500.0)
    )
    conn.commit()

    print('Начальные балансы:')
    for row in cur.execute('SELECT * FROM accounts'):
        print(row)

    print('\n--- Демонстрация отката (ROLLBACK) ---')
    try:
        cur.execute('UPDATE accounts SET balance = balance - 500 WHERE id = 1')
        cur.execute('UPDATE accounts SET balance = balance + 500 WHERE id = 2')
        
        # Представим, что произошла ошибка (например, проверка)
        raise ValueError('Искусственная ошибка!')
        
        conn.commit()  # Не выполнится
    except ValueError as e:
        print(f'Ошибка: {e}')
        conn.rollback()
        print('Транзакция отменена (ROLLBACK).')

    print('\nБалансы после отката (должны быть исходными):')
    for row in cur.execute('SELECT * FROM accounts'):
        print(row)

    conn.close()


if __name__ == '__main__':
    main()
