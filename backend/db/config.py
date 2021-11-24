from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import Settings


engine = create_async_engine(Settings.DATABASE_URL, future=True, echo=True)
async_db_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
BaseModel = declarative_base()
