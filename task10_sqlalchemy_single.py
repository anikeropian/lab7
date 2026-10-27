from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройка SQLite и SQLAlchemy
engine = create_engine('sqlite:///users_orm.db')
Base = declarative_base()


class User(Base):
    """Модель пользователя для SQLAlchemy."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f'<User(id={self.id}, name={self.name}, age={self.age})>'


# Создание таблицы
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def main():
    """Демонстрация работы SQLAlchemy ORM."""
    session = Session()

    # Очистка для чистоты
    session.query(User).delete()
    session.commit()

    # Добавление данных через ORM
    user1 = User(name='Алексей', age=30)
    user2 = User(name='Ольга', age=28)
    session.add_all([user1, user2])
    session.commit()

    print('--- Пользователи в БД (ORM) ---')
    users = session.query(User).all()
    for user in users:
        print(user)

    session.close()


if __name__ == '__main__':
    main()
