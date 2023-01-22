from pydantic import BaseModel
from models import Statistic

class UserSchema(BaseModel):
    analysis: int
    signals: int
    screenshot: int
    help: int



async def create_user(user: UserSchema):
    user = await Statistic.create(**user.dict())
    return user



async def get_user(id: str):
    user = await Statistic.get(id)
    return user



async def get_all_users():
    users = await Statistic.get_all()
    return users



async def update(id: str, user: UserSchema):
    user = await Statistic.update(id, **user.dict())
    return user



async def delete_user(id: str):
    return await Statistic.delete(id)