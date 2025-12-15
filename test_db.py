from sqlalchemy import text
from app.core.database import sync_engine

print("Connecting...")
with sync_engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("SELECT 1 ->", result.scalar())
print("OK")
