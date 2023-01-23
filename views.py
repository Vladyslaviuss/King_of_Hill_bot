from pydantic import BaseModel
from models import Statistic

class StringSchema(BaseModel):
    analysis: int
    signals: int
    screenshot: int
    help: int



async def create_user(new_db_string: StringSchema):
    new_db_string = await Statistic.create(**new_db_string.dict())
    return new_db_string



async def get_user(id: str):
    new_db_string = await Statistic.get(id)
    return new_db_string



async def get_all_users():
    new_db_strings = await Statistic.get_all()
    return new_db_strings



async def update(id: str, new_db_string: StringSchema):
    new_db_string = await Statistic.update(id, **new_db_string.dict())
    return new_db_string



async def delete_user(id: str):
    return await Statistic.delete(id)