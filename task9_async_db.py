import asyncio
import databases
import sqlalchemy

# Настройка асинхронного подключения к SQLite
DATABASE_URL = 'sqlite:///async.db'
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)


async def main():
    """Демонстрация асинхронной работы с БД."""
    await database.connect()
    print('Асинхронное подключение к БД установлено.')

    # Вставка
    query = users.insert().values(name='Асинхронный пользователь')
    last_id = await database.execute(query)
    print(f'Вставлена запись с ID: {last_id}')

    # Чтение
    query = users.select()
    rows = await database.fetch_all(query)
    print('Все пользователи в БД:')
    for row in rows:
        print(dict(row))

    await database.disconnect()
    print('Подключение закрыто.')


if __name__ == '__main__':
    asyncio.run(main())
