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


async def create_chat_entry(chat_id, new_db_string: StringSchema):
    new_db_string = await Statistic.create(chat_id, **new_db_string.dict())
    return new_db_string


async def create_user_entry(telegram_user_id, chat_id, new_db_string: IndividualSchema):
    new_db_string = await Individual.create(telegram_user_id, chat_id, **new_db_string.dict())
    return new_db_string


async def update_chat_parameter_or_target(chat_id: int, existed_db_string: StringSchema | TargetSchema):
    return await Statistic.update(chat_id, **existed_db_string.dict())


async def update_user_parameter(telegram_user_id: int, existed_db_string: IndividualSchema):
    return await Individual.update(telegram_user_id, **existed_db_string.dict())


async def update_overall_statistic_table(chat_id: int, text:str):
    # Retrieve the existing entry from the database
    same_db_string = await Statistic.get(chat_id)

    # Define a dictionary to map the text input to the corresponding field and operation
    field_map = {
        '+': ('screenshot', 1, "Параметр 'Скрины со сделками'"),
        '-': ('screenshot', -1, "Параметр 'Скрины со сделками'"),
        '++': ('signals', 1, "Параметр 'Сигналы-детекты'"),
        '--': ('signals', -1, "Параметр 'Сигналы-детекты'"),
        '+++': ('help', 1, "Параметр 'Помощь новичкам, ответы на вопросы'"),
        '---': ('help', -1, "Параметр 'Помощь новичкам, ответы на вопросы'"),
        '++++': ('analysis', 1, "Параметр 'Разбор своих сделок'"),
        '----': ('analysis', -1, "Параметр 'Разбор своих сделок'")
    }
    # Get the field and operation from the field_map
    field, operation, message = field_map.get(text, (None, None, None))
    if field:
        # Perform the operation on the specified field
        setattr(same_db_string, field, getattr(same_db_string, field) + operation)
        message_text = f"{message} у{'величен' if operation > 0 else 'меньшен'} на 1."
        # Convert the updated object to a dictionary
        updated_values = same_db_string.__dict__
        # Call the update function to save the updated values to the database
        await update_chat_parameter_or_target(chat_id, existed_db_string=StringSchema(**updated_values))
        return message_text


async def update_individual_statistic_table(telegram_user_id: int, text:str):
    points_mapping = {
        "+": (1, "screenshot"),
        "++": (2, "signals"),
        "+++": (5, "help"),
        "++++": (10, "analysis"),
    }
    # Retrieve the existing entry from the database
    same_db_string = await Individual.get(telegram_user_id)
    if text in points_mapping:
        points, field = points_mapping[text]
        setattr(same_db_string, field, getattr(same_db_string, field) + 1)
        same_db_string.points += points
        message_text = f"Пользователь @{same_db_string.username} получает {points} очков."
        # Convert the updated object to a dictionary
        updated_values = same_db_string.__dict__
        # Call the update function to save the updated values to the database
        await update_user_parameter(telegram_user_id, existed_db_string=IndividualSchema(**updated_values))
        return message_text

async def set_the_value_for_parameter(chat_id: int, param: int, value: int):
    same_db_string = await Statistic.get(chat_id)
    if param > 4:
        return '🧐 Первая цифра должна быть не больше 4, соответствуя номеру каждого существующего параметра.'

    param_mapping = {
        1: ('screenshot', 'Скрины со сделками'),
        2: ('signals', 'Сигналы-детекты'),
        3: ('help', 'Помощь новичкам, ответы на вопросы'),
        4: ('analysis', 'Разбор своих сделок')
    }
    param_name, output_name = param_mapping.get(param)
    if param_name:
        setattr(same_db_string, param_name, value)
        message_text = f"Параметр '{output_name}' увеличен до значения: {value}."
    else:
        message_text = f'Параметр с номером {param} не найден.'

    updated_values = same_db_string.__dict__
    await update_chat_parameter_or_target(chat_id, existed_db_string=StringSchema(**updated_values))
    return message_text


async def set_the_target_for_parameter(chat_id: int, param: int, target: int):
    # Retrieve the existing entry from the database
    same_db_string = await Statistic.get(chat_id)
    if param > 4:
        return '🧐 Первая цифра должна быть не больше 4, соответствуя номеру каждого существующего параметра.'

    param_mapping = {
        1: ('screenshot_target', 'Скрины со сделками'),
        2: ('signals_target', 'Сигналы-детекты'),
        3: ('help_target', 'Помощь новичкам, ответы на вопросы'),
        4: ('analysis_target', 'Разбор своих сделок')
    }
    param_name, output_name = param_mapping.get(param)
    if param_name:
        setattr(same_db_string, param_name, target)
        message_text = f"Новая цель для параметра '{output_name}' установлена: {target}."
    else:
        message_text = f'Параметр с номером {param} не найден.'
    # if param <= 4:
    #     if param == 1:
    #     # Increase the analysis field by 1
    #         same_db_string.analysis_target = target
    #         message_text = f"Новая цель для параметра 'Разбор своих сделок' установлена: {target}."
    #     elif param == 2:
    #         same_db_string.signals_target = target
    #         message_text = f"Новая цель для параметра 'Сигналы-детекты' установлена: {target}."
    #     elif param == 3:
    #         same_db_string.screenshot_target = target
    #         message_text = f"Новая цель для параметра 'Скрины со сделками' установлена: {target}."
    #     elif param == 4:
    #         same_db_string.help_target = target
    #         message_text = f"Новая цель для параметра 'Помощь новичкам, ответы на вопросы' установлена: {target}."
    # else:
    #     message_text = f'🧐 Первая цифра должна быть не больше 4, соответствуя номеру каждого существующего параметра.'
    # Convert the updated object to a dictionary
    updated_values = same_db_string.__dict__
    # Call the update function to save the updated values to the database
    await update_chat_parameter_or_target(chat_id, existed_db_string=TargetSchema(**updated_values))
    return message_text






