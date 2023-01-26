import random

from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from database import Base, db



class Statistic(Base):
    __tablename__ = "overall_statistic"
    chat_id = Column(BigInteger, primary_key=True)
    analysis = Column(Integer)
    signals = Column(Integer)
    screenshot = Column(Integer)
    help = Column(Integer)
    analysis_target = Column(Integer, default=10)
    signals_target = Column(Integer, default=20)
    screenshot_target = Column(Integer, default=90)
    help_target = Column(Integer, default=20)

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
    async def create(cls, chat_id, **kwargs):
        new_db_string = cls(chat_id=chat_id, **kwargs)
        db.add(new_db_string)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return new_db_string

    @classmethod
    async def update(cls, chat_id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.chat_id == chat_id)
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
    async def get(cls, chat_id):
        query = select(cls).where(cls.chat_id == chat_id)
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
    async def delete(cls, chat_id):
        query = sqlalchemy_delete(cls).where(cls.chat_id == chat_id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True


class Individual(Base):
    __tablename__ = "individual_statistic"
    chat_id = Column(BigInteger, ForeignKey("overall_statistic.chat_id"))
    telegram_user_id = Column(BigInteger, primary_key=True)
    username = Column(String)
    analysis = Column(Integer)
    signals = Column(Integer)
    screenshot = Column(Integer)
    help = Column(Integer)
    points = Column(Integer)

    def __str__(self):
        return (
            f"\nСкрины со сделками: {self.screenshot}\n"
            f"Сигналы-детекты: {self.signals}\n"
            f"Помощь новичкам, ответы на вопросы: {self.help}\n"
            f"Разбор своих сделок: {self.analysis}\n"
            f"\nЗаработанные очки: {self.points}"
        )

    @classmethod
    async def create(cls, telegram_user_id, chat_id, **kwargs):
        new_db_string = cls(telegram_user_id=telegram_user_id, chat_id=chat_id, **kwargs)
        db.add(new_db_string)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return new_db_string

    @classmethod
    async def update(cls, telegram_user_id, username, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.telegram_user_id == telegram_user_id)
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
    async def get(cls, telegram_user_id):
        query = select(cls).where(cls.telegram_user_id == telegram_user_id)
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
    async def delete(cls, telegram_user_id):
        query = sqlalchemy_delete(cls).where(cls.telegram_user_id == telegram_user_id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True