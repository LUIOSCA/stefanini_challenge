import asyncio
from app.core.database import engine, Base
from app.api.v1.users.models import User

async def reset_db():
    async with engine.begin() as conn:
        print("Dropping tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Creating tables with new constraints...")
        await conn.run_sync(Base.metadata.create_all)
    print("Database schema updated successfully.")

if __name__ == "__main__":
    asyncio.run(reset_db())