# backend/app/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm         import sessionmaker, declarative_base
from sqlalchemy.engine.url  import make_url

# load the raw URL
raw_url = os.getenv("DATABASE_URL")

# parse & ensure it's asyncpg
url = make_url(raw_url)
if url.drivername in ("postgresql", "postgres"):
    url = url.set_drivername("postgresql+asyncpg")

# create the async engine
engine = create_async_engine(url, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session() as session:
        yield session
