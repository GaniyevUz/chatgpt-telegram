from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from data.config import DB_URL

# engine = create_engine(db_url)
#
#
# def get_session(autocommit=False):
#     return sessionmaker(bind=engine, autocommit=autocommit).begin()


engine = create_async_engine(
    DB_URL,
    future=True,
    # echo=True,
    pool_size=20,  # set the maximum number of connections in the connection pool
    max_overflow=30,  # set the maximum number of connections that can be created above the pool_size
)
# Base = declarative_base()

# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True)
AsyncScopedSession = async_scoped_session(async_session, scopefunc=current_task)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        finally:
            await session.close()
