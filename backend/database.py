
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker, AsyncSession
import os 
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv('POSTGRES_URL')
engine=create_async_engine(
    DATABASE_URL,
)


AsyncSessionLocal=async_sessionmaker(
    class_=AsyncSession, bind=engine, autoflush=True
)

Base=declarative_base()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session   
        except Exception as e:
            session.rollback()