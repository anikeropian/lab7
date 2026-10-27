import sqlite3


def setup_db():
    """Создаёт БД и таблицу, если их нет."""
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    return conn


def main():
    """Демонстрация параметров запроса и обновления записи."""
    conn = setup_db()
    cur = conn.cursor()

    # Очистим таблицу для чистоты эксперимента
    cur.execute('DELETE FROM users')
    conn.commit()

    # Задание №6: Использование параметров запроса (безопасный INSERT)
    # Знаки ? защищают от SQL-инъекций
    users_to_insert = [('Ани', 20), ('Иван', 22), ('Мария', 19)]
    cur.executemany('INSERT INTO users (name, age) VALUES (?, ?)', users_to_insert)
    conn.commit()
    print('--- Добавлены пользователи (Задание №6) ---')

    # Чтение с параметром
    target_id = 1
    cur.execute('SELECT * FROM users WHERE id = ?', (target_id,))
    print(f'До обновления ID {target_id}:', cur.fetchone())

    # Задание №4: Обновление записи
    new_age = 25
    cur.execute(
        'UPDATE users SET age = ? WHERE id = ?',
        (new_age, target_id)
    )
    conn.commit()

    # Проверка обновления
    cur.execute('SELECT * FROM users WHERE id = ?', (target_id,))
    print(f'После обновления ID {target_id}:', cur.fetchone())
    print('(Возраст изменён с 20 на 25)')

    conn.close()


if __name__ == '__main__':
    main()
