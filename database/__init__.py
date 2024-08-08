from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session, declarative_base


# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
# engine = create_async_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# создадим или подключимся к базе данных
SQLALCHEMY_BASE_URL = "sqlite:///book_listening.db"
# создаем движок
engine = create_engine(SQLALCHEMY_BASE_URL)
# переменная, которая будет генерировать сессии
SessionLocal = sessionmaker(bind=engine)
# создадим шаблон декларативной базы данных для классов (Model...)
Base = declarative_base()

# функция-генератор сессий и отката бд
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()