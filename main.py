import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ContentType, ChatMemberStatus
from database import Base, db
# from pydantic import BaseModel
# from models import Statistic
# from database import Base
from views import get_string, update, StringSchema

TELEGRAM_BOT_TOKEN = '5602947939:AAFMRW-ElOh7FgQFHvmssoSCMtPhu3nm-18'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

db.init()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    result = await get_string('9056955f-9032-4d52-9211-68c990fa02e7')
    await message.reply(f"Hi!\nI'm Bot!\n First data in db written! {result}")

    # async def update(id: str, new_db_string: StringSchema):
    #     new_db_string = await Statistic.update(id, **new_db_string.dict())
    #     return new_db_string

@dp.message_handler(content_types=ContentType.TEXT)
async def handle_text(message: Message):
    text = message.text.lower()
    member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status == ChatMemberStatus.OWNER:
        if message.reply_to_message:
            if not message.reply_to_message.from_user.is_bot:
                # if not user_data:
                #     user_data = {'Разбор своих сделок': 0, 'Сигналы-детекты': 0, 'Скрины со сделками': 0,
                #                  'Помощь новичкам, ответы на вопросы': 0}
                if text == '+':
                    # user_data['Разбор своих сделок'] += 1
                    result = await update(id='9056955f-9032-4d52-9211-68c990fa02e7', existed_db_string=StringSchema(analysis=5, signals=5, screenshot=2, help=1))
                    message_text = f'Нажал на + и получил: {result}.'
                    await bot.send_message(chat_id=message.chat.id, text=message_text)
                # elif text == '-':
                #     user_data['Разбор своих сделок'] -= 1
                #     message_text = f'Параметр "Разбор своих сделок" уменьшен на 1. Текущее значение: {user_data["Разбор своих сделок"]}.'
                #     await bot.send_message(chat_id=message.chat.id, text=message_text)
                # elif text == '++':
                #     user_data['Сигналы-детекты'] += 1
                #     message_text = f'Параметр "Сигналы-детекты" увеличен на 1. Текущее значение: {user_data["Сигналы-детекты"]}.'
                #     await bot.send_message(chat_id=message.chat.id, text=message_text)
                # elif text == '--':
                #     user_data['Сигналы-детекты'] -= 1
                #     message_text = f'Параметр "Сигналы-детекты" уменьшен на 1. Текущее значение: {user_data["Сигналы-детекты"]}.'
                #     await bot.send_message(chat_id=message.chat.id, text=message_text)
                # elif text == '+++':
                #     user_data['Скрины со сделками'] += 1
                #     message_text = f'Параметр "Скрины со сделками" увеличен на 1. Текущее значение: {user_data["Скрины со сделками"]}.'
                #     await bot.send_message(chat_id=message.chat.id, text=message_text)
                # elif text == '---':
                #     user_data['Скрины со сделками'] -= 1
                #     message_text = f'Параметр "Скрины со сделками" уменьшен на 1. Текущее значение: {user_data["Скрины со сделками"]}.'
                #     await bot.send_message(chat_id=message.chat.id, text=message_text)
                # elif text == '++++':
                #     user_data['Помощь новичкам, ответы на вопросы'] += 1
                #     message_text = f'Параметр "Помощь новичкам, ответы на вопросы" увеличен на 1. Текущее значение: {user_data["Помощь новичкам, ответы на вопросы"]}.'
                #     await bot.send_message(chat_id=message.chat.id, text=message_text)
                # elif text == '----':
                #     user_data['Помощь новичкам, ответы на вопросы'] -= 1
                #     message_text = f'Параметр "Помощь новичкам, ответы на вопросы" уменьшен на 1. Текущее значение: {user_data["Помощь новичкам, ответы на вопросы"]}.'
                #     await bot.send_message(chat_id=message.chat.id, text=message_text)
            else:
                message_text = "Can't add or subtract parameters to a bot."
                await bot.send_message(chat_id=message.chat.id, text=message_text)
    else:
        message_text = "You have no permission"
        await bot.send_message(chat_id=message.chat.id, text=message_text)

async def startup():
    await db.create_all()

    await dp.start_polling(bot)





if __name__ == '__main__':
    asyncio.run(startup())

