import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ContentType, ChatMemberStatus
from database import Base, db
from models import Statistic
# from pydantic import BaseModel
# from models import Statistic
# from database import Base
from views import get_string, StringSchema, update_the_value_of_object, check_if_exists, create_new_string

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
    member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status == ChatMemberStatus.OWNER:
        await message.reply("Hi!\nI'm Bot!\n This is test message.")
    else:
        await message.reply("You have no permission")

@dp.message_handler(commands=['results'])
async def show_results(message: types.Message):
    """
    This handler will be called when user sends the command '/results' as reply for message
    """
    if await check_if_exists(id=message.chat.id) is not None:
        results = await get_string(id=message.chat.id)
        message_text = f'\nОбщие результаты:\n'
        message_text += f'\n{results}\n'
        await message.reply(f"{message_text}")
    else:
        await bot.send_message(
            chat_id=message.chat.id, text=f'Currently no any results for chat "{message.chat.full_name}".'
        )

@dp.message_handler(content_types=ContentType.TEXT)
async def handle_text(message: Message):
    text = message.text.lower()
    member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status == ChatMemberStatus.OWNER:
        if message.reply_to_message:
            if not message.reply_to_message.from_user.is_bot:
                if await check_if_exists(id=message.chat.id) is None:
                    await create_new_string(id=message.chat.id, new_db_string=StringSchema(analysis=0, signals=0, screenshot=0, help=0))
                    message_text = f'Записи не найдены. Параметры для Вашего чата: "{message.chat.full_name}" сгенерированы. Повторите последнее действие для его применения.'
                    await bot.send_message(chat_id=message.chat.id, text=message_text)
                else:
                    result = await update_the_value_of_object(id=message.chat.id, text=text)
                    message_text = f'{result}'
                    await bot.send_message(chat_id=message.chat.id, text=message_text)
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

