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



async def update_the_value_of_object(id: str, text:str):
    # Retrieve the existing entry from the database
    same_db_string = await Statistic.get(id)
    if text == '+':
    # Increase the analysis field by 1
        same_db_string.analysis += 1
    elif text == '-':
        same_db_string.analysis -= 1
    elif text == '++':
        same_db_string.signals += 1
    elif text == '--':
        same_db_string.signals -= 1
    elif text == '+++':
        same_db_string.screenshot += 1
    elif text == '---':
        same_db_string.screenshot -= 1
    elif text == '++++':
        same_db_string.help += 1
    elif text == '----':
        same_db_string.help -= 1

    # Convert the updated object to a dictionary
    updated_values = same_db_string.__dict__

    # Call the update function to save the updated values to the database
    await update(id,existed_db_string=StringSchema(**updated_values))
    return await get_string(id)

# async def check_if_exists(id: str):
#     try:
#         query = select([Statistic]).where(Statistic.id == id)
#         result = await db.execute(query)
#         if result.scalars().first() is None:
#             return False
#         else:
#             return True
#     except Exception as e:
#         print(f"Error connecting to the database: {e}")
#         return False

async def check_if_exists(id: str):
    # Try to retrieve the record with the specific ID
    result = await Statistic.get(id)
    # Check if the result is None
    if result is not None:
        return True
    else:
        return False

