from pydantic import BaseModel
from models import Statistic

class StringSchema(BaseModel):
    analysis: int
    signals: int
    screenshot: int
    help: int



async def create_new_string(id, new_db_string: StringSchema):
    new_db_string = await Statistic.create(id, **new_db_string.dict())
    return new_db_string



async def get_string(id: int):
    new_db_string = await Statistic.get(id)
    return new_db_string



async def get_all_strings():
    new_db_strings = await Statistic.get_all()
    return new_db_strings



async def update(id: int, existed_db_string: StringSchema):
    same_db_string = await Statistic.update(id, **existed_db_string.dict())
    return same_db_string



async def delete_string(id: int):
    return await Statistic.delete(id)



async def update_the_value_of_object(id: int, text:str):
    # Retrieve the existing entry from the database
    same_db_string = await Statistic.get(id)
    if text == '+':
    # Increase the analysis field by 1
        same_db_string.analysis += 1
        message_text = "Параметр 'Разбор своих сделок' увеличен на 1."
    elif text == '-':
        same_db_string.analysis -= 1
        message_text = "Параметр 'Разбор своих сделок' уменьшен на 1."
    elif text == '++':
        same_db_string.signals += 1
        message_text = "Параметр 'Сигналы-детекты' увеличен на 1."
    elif text == '--':
        same_db_string.signals -= 1
        message_text = "Параметр 'Сигналы-детекты' уменьшен на 1."
    elif text == '+++':
        same_db_string.screenshot += 1
        message_text = "Параметр 'Скрины со сделками' увеличен на 1."
    elif text == '---':
        message_text = "Параметр 'Скрины со сделками' уменьшен на 1."
        same_db_string.screenshot -= 1
    elif text == '++++':
        same_db_string.help += 1
        message_text = "Параметр 'Помощь новичкам, ответы на вопросы' увеличен на 1."
    elif text == '----':
        same_db_string.help -= 1
        message_text = "Параметр 'Помощь новичкам, ответы на вопросы' уменьшен на 1."

    # Convert the updated object to a dictionary
    updated_values = same_db_string.__dict__

    # Call the update function to save the updated values to the database
    await update(id,existed_db_string=StringSchema(**updated_values))
    return message_text

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

async def check_if_exists(id: int):
    # Try to retrieve the record with the specific ID
    result = await Statistic.get(id)
    # Check if the result is None
    # if result is not None:
    #     return True
    # else:
    #     return False
    return result


async def set_the_value_for_exact_parameter(id: int, param: int, value: int):
    # Retrieve the existing entry from the database
    same_db_string = await Statistic.get(id)
    if param <= 4:
        if param == 1:
        # Increase the analysis field by 1
            same_db_string.analysis = value
            message_text = f"Параметр 'Разбор своих сделок' увеличен до значения: {value}."
        elif param == 2:
            same_db_string.signals = value
            message_text = f"Параметр 'Сигналы-детекты' увеличен до значения: {value}."
        elif param == 3:
            same_db_string.screenshot = value
            message_text = f"Параметр 'Скрины со сделками' увеличен до значения: {value}."
        elif param == 4:
            same_db_string.help = value
            message_text = f"Параметр 'Помощь новичкам, ответы на вопросы' увеличен до значения: {value}."
    else:
        message_text = f'Первая цифра должна быть не больше 4, соответствуя номеру каждого существующего параметра.'
    # Convert the updated object to a dictionary
    updated_values = same_db_string.__dict__

    # Call the update function to save the updated values to the database
    await update(id,existed_db_string=StringSchema(**updated_values))
    return message_text

