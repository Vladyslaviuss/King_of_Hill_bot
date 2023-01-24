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

async def update(id: str, existed_db_string: StringSchema):
    same_db_string = await Statistic.update(id, **existed_db_string.dict())
    return same_db_string




@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    result = await get_string('26fd2706-8baf-433b-82eb-8c7fada847da')
    await message.reply(f"Hi!\nI'm Bot!\n First data in db written! {result}")



@dp.message_handler(content_types=ContentType.TEXT)
async def handle_text(message: Message):
    text = message.text.lower()
    member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status == ChatMemberStatus.OWNER:
        if message.reply_to_message:
            if not message.reply_to_message.from_user.is_bot:
                if await check_if_exists(id=message.chat.id) is None:
                    await create_new_string(id=message.chat.id, new_db_string=StringSchema(analysis=0, signals=0, screenshot=0, help=0))
                else:
                    result = await update_the_value_of_object(id=message.chat.id, text=text)
                    message_text = f'Нажал на {text} и получил: {result}.'
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

