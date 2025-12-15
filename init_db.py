from app.core.database import sync_engine, Base

from app.models import employee, task

def init_db():
    print("Создаём таблицы...")
    Base.metadata.create_all(bind=sync_engine)
    print("Готово.")

if __name__ == "__main__":
    init_db()
