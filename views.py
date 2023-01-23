from pydantic import BaseModel
from models import Statistic

class StringSchema(BaseModel):
    analysis: int
    signals: int
    screenshot: int
    help: int



async def create_new_string(new_db_string: StringSchema):
    new_db_string = await Statistic.create(**new_db_string.dict())
    return new_db_string



async def get_string(id: str):
    new_db_string = await Statistic.get(id)
    return new_db_string



async def get_all_strings():
    new_db_strings = await Statistic.get_all()
    return new_db_strings



async def update(id: str, existed_db_string: StringSchema):
    same_db_string = await Statistic.update(id, **existed_db_string.dict())
    return same_db_string



async def delete_string(id: str):
    return await Statistic.delete(id)