from sqlalchemy import text
from app.core.config import settings
from app.core.database import sync_engine

print("DB URL:", settings.database_url_syncpg)
print("Engine URL:", sync_engine.url)
with sync_engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("SELECT 1 ->", result.scalar())
print(conn.execute(text("SELECT 1")).scalar())
