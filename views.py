from pydantic import BaseModel
from models import Statistic, Individual

class StringSchema(BaseModel):
    analysis: int
    signals: int
    screenshot: int
    help: int

class TargetSchema(BaseModel):
    analysis_target: int
    signals_target: int
    screenshot_target: int
    help_target: int

class IndividualSchema(BaseModel):
    username: str
    analysis: int
    signals: int
    screenshot: int
    help: int
    points: int


async def create_new_string(chat_id, new_db_string: StringSchema):
    new_db_string = await Statistic.create(chat_id, **new_db_string.dict())
    return new_db_string



async def get_string(chat_id: int):
    new_db_string = await Statistic.get(chat_id)
    return new_db_string

async def get_user(telegram_user_id: int):
    new_db_string = await Individual.get(telegram_user_id)
    return new_db_string



async def get_all_strings():
    new_db_strings = await Statistic.get_all()
    return new_db_strings



async def update(chat_id: int, existed_db_string: StringSchema | TargetSchema):
    same_db_string = await Statistic.update(chat_id, **existed_db_string.dict())
    return same_db_string

async def update2(telegram_user_id: int, existed_db_string: IndividualSchema):
    same_db_string = await Individual.update(telegram_user_id, **existed_db_string.dict())
    return same_db_string



async def update_target(chat_id: int, existed_db_string: dict):
    same_db_string = await Statistic.update(chat_id, **existed_db_string)
    return same_db_string



async def delete_string(chat_id: int):
    return await Statistic.delete(chat_id)



async def update_the_value_of_object(chat_id: int, text:str):
    # Retrieve the existing entry from the database
    same_db_string = await Statistic.get(chat_id)
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
    await update(chat_id,existed_db_string=StringSchema(**updated_values))
    return message_text


async def check_if_exists(chat_id: int):
    # Try to retrieve the record with the specific ID
    result = await Statistic.get(chat_id)
    return result


async def set_the_value_for_exact_parameter(chat_id: int, param: int, value: int):
    # Retrieve the existing entry from the database
    same_db_string = await Statistic.get(chat_id)
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
    await update(chat_id,existed_db_string=StringSchema(**updated_values))
    return message_text


async def set_the_target_for_exact_parameter(chat_id: int, param: int, target: int):
    # Retrieve the existing entry from the database
    same_db_string = await Statistic.get(chat_id)
    if param <= 4:
        if param == 1:
        # Increase the analysis field by 1
            same_db_string.analysis_target = target
            message_text = f"Новая цель для параметра 'Разбор своих сделок' установлена: {target}."
        elif param == 2:
            same_db_string.signals_target = target
            message_text = f"Новая цель для параметра 'Сигналы-детекты' установлена: {target}."
        elif param == 3:
            same_db_string.screenshot_target = target
            message_text = f"Новая цель для параметра 'Скрины со сделками' установлена: {target}."
        elif param == 4:
            same_db_string.help_target = target
            message_text = f"Новая цель для параметра 'Помощь новичкам, ответы на вопросы' установлена: {target}."
    else:
        message_text = f'Первая цифра должна быть не больше 4, соответствуя номеру каждого существующего параметра.'
    # Convert the updated object to a dictionary
    updated_values = same_db_string.__dict__

    # Call the update function to save the updated values to the database
    await update(chat_id,existed_db_string=TargetSchema(**updated_values))
    return message_text



async def create_new_userdata(telegram_user_id, chat_id, new_db_string: IndividualSchema):
    new_db_string = await Individual.create(telegram_user_id, chat_id, **new_db_string.dict())
    return new_db_string

async def existance_of_user(telegram_user_id: int):
    # Try to retrieve the record with the specific ID
    result = await Individual.get(telegram_user_id)
    return result

async def update_user_parameter(telegram_user_id: int, text:str):
    # Retrieve the existing entry from the database
    same_db_string = await Individual.get(telegram_user_id)
    if text == '+':
    # Increase the analysis field by 1
        same_db_string.analysis += 1
        same_db_string.points += 10
        message_text = f"Пользователь @{same_db_string.username} получает 10 очков."
    # elif text == '-':
    #     same_db_string.analysis -= 1
    #     message_text = f"Параметр 'Разбор своих сделок' уменьшен на 1. for {same_db_string.username}."
    elif text == '++':
        same_db_string.signals += 1
        same_db_string.points += 2
        message_text = f"Пользователь @{same_db_string.username} получает 2 очка."
    # elif text == '--':
    #     same_db_string.signals -= 1
    #     message_text = f"Параметр 'Сигналы-детекты' уменьшен на 1. for {same_db_string.username}."
    elif text == '+++':
        same_db_string.screenshot += 1
        same_db_string.points += 1
        message_text = f"Пользователь @{same_db_string.username} получает 1 очко."
    # elif text == '---':
    #     message_text = f"Параметр 'Скрины со сделками' уменьшен на 1. for {same_db_string.username}."
    #     same_db_string.screenshot -= 1
    elif text == '++++':
        same_db_string.help += 1
        same_db_string.points += 5
        message_text = f"Пользователь @{same_db_string.username} получает 5 очков."
    # elif text == '----':
    #     same_db_string.help -= 1
    #     message_text = f"Параметр 'Помощь новичкам, ответы на вопросы' уменьшен на 1. for {same_db_string.username}."

    # Convert the updated object to a dictionary
    updated_values = same_db_string.__dict__

    # Call the update function to save the updated values to the database
    await update2(telegram_user_id,existed_db_string=IndividualSchema(**updated_values))
    return message_text


async def check_content(chat_id: int):
    result = await Individual.table_content(chat_id)
    return result


async def show_leaders(qtty: int):
    result = await Individual.get_top_users_by_points(qtty=qtty)
    return result