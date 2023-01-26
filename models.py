import random

from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from database import Base, db



class Statistic(Base):
    __tablename__ = "overall_statistic"
    id = Column(BigInteger, primary_key=True)
    analysis = Column(Integer)
    signals = Column(Integer)
    screenshot = Column(Integer)
    help = Column(Integer)
    analysis_target = Column(Integer, default=10)
    signals_target = Column(Integer, default=20)
    screenshot_target = Column(Integer, default=90)
    help_target = Column(Integer, default=20)

    # def __repr__(self):
    #     return (
    #         f"<{self.__class__.__name__}("
    #         f"id={self.id}, "
    #         f"analysis={self.analysis}, "
    #         f")>"
    #     )

    def __str__(self):
        full_message = ''
        if self.analysis <= self.analysis_target:
            message = f"1. ({self.analysis} / {self.analysis_target} шт) Разбор своих сделок\n"
            full_message += message
        else:
            message = f"1. ({self.analysis} / {self.analysis_target} шт) ✅ Разбор своих сделок\n"
            full_message += message
        if self.signals <= self.signals_target:
            message = f"2. ({self.signals} / {self.signals_target} шт) Сигналы-детекты\n"
            full_message += message
        else:
            message = f"2. ({self.signals} / {self.signals_target} шт) ✅ Сигналы-детекты\n"
            full_message += message
        if self.screenshot <= self.screenshot_target:
            message = f"3. ({self.screenshot} / {self.screenshot_target} шт) Скрины со сделками\n"
            full_message += message
        else:
            message = f"3. ({self.screenshot} / {self.screenshot_target} шт) ✅ Скрины со сделками\n"
            full_message += message
        if self.help <= self.help_target:
            message = f"4. ({self.help} / {self.help_target} шт) Помощь новичкам, ответы на вопросы\n"
            full_message += message
        else:
            message = f"4. ({self.help} / {self.help_target} шт) ✅ Помощь новичкам, ответы на вопросы\n"
            full_message += message
        return full_message

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


class Individual(Base):
    __tablename__ = "individual_statistic"
    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    analysis = Column(Integer)
    signals = Column(Integer)
    screenshot = Column(Integer)
    help = Column(Integer)

    def __str__(self):
        return (
            f"Индивидуальный вклад пользователя {self.username} за все время:\n"
            f"\nСкрины со сделками: {self.screenshot}"
            f"Сигналы-детекты: {self.signals}"
            f"Помощь новичкам, ответы на вопросы: {self.help}"
            f"Разбор своих сделок: {self.analysis}"
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
    async def update(cls, id, username, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(username=username, **kwargs)
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