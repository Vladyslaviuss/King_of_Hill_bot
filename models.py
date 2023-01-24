import random

from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from database import Base, db
from uuid import uuid4
from aiogram.types import Message


class Statistic(Base):
    __tablename__ = "hilldb"
    id = Column(BigInteger, primary_key=True)
    analysis = Column(Integer)
    signals = Column(Integer)
    screenshot = Column(Integer)
    help = Column(Integer)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"analysis={self.analysis}, "
            f")>"
        )

    @classmethod
    async def create(cls, id, **kwargs):
        new_db_string = cls(id=id, **kwargs)
        db.add(new_db_string)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return new_db_string

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        new_db_strings = await db.execute(query)
        try:
            (new_db_string,) = new_db_strings.first()
            return new_db_string
        except TypeError as e:
            return None
        # if new_db_string is None:
        #     return None
        # else:
        #     unpacked = (new_db_string,)
        #     return unpacked

    @classmethod
    async def get_all(cls):
        query = select(cls)
        new_db_strings = await db.execute(query)
        new_db_strings = new_db_strings.scalars().all()
        return new_db_strings

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True