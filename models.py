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
        tasks = [
            {'name': 'Разбор своих сделок', 'current': self.analysis, 'target': self.analysis_target},
            {'name': 'Сигналы-детекты', 'current': self.signals, 'target': self.signals_target},
            {'name': 'Скрины со сделками', 'current': self.screenshot, 'target': self.screenshot_target},
            {'name': 'Помощь новичкам, ответы на вопросы', 'current': self.help, 'target': self.help_target}
        ]
        for i, task in enumerate(tasks, 1):
            if task['current'] < task['target']:
                message = f"{i}. ({task['current']} / {task['target']} шт) {task['name']}\n"
            else:
                message = f"{i}. ({task['current']} / {task['target']} шт) ✅ {task['name']}\n"
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
        except TypeError:
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
    @classmethod
    async def get_top_users_by_points(cls, qtty):
        top_users = await db.execute(select(cls).order_by(cls.points.desc()).limit(qtty))
        top_users = top_users.scalars().all()
        top_users_str = [f"{i}. @{user.username} - {user.points} point(s)" for i, user in enumerate(top_users, 1)]
        return "\n".join(top_users_str)

    @classmethod
    async def table_content(cls, chat_id: int):
        query = select(cls).where(cls.chat_id == chat_id)
        result = await db.execute(query)
        # True - means there are rows with the specified chat_id
        # None - means there are no rows with the specified chat_id
        return True if result.scalar() else None



