
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

class Base(DeclarativeBase):
    pass

# connection_string = f"postgresql+psycopg2://{os.getenv('DEV_DATABASE_USER')}:{os.getenv('DEV_DATABASE_PASSWORD')}@{os.getenv('DEV_DATABASE_HOST')}:5432/{os.getenv('DEV_DATABASE_NAME')}"
connection_string = f"postgresql+asyncpg://{os.getenv('DEV_DATABASE_USER')}:{os.getenv('DEV_DATABASE_PASSWORD')}@{os.getenv('DEV_DATABASE_HOST')}:5432/{os.getenv('DEV_DATABASE_NAME')}"

engine = create_async_engine(connection_string, echo=True)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

async def get_db():
    async with engine.connect() as conn:
        yield conn