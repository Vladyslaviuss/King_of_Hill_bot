import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ContentType, ChatMemberStatus
from aiogram.utils import executor
from database import db
from models import Statistic
from views import get_string, StringSchema, update_the_value_of_object, check_if_exists, \
    create_new_string, set_the_value_for_exact_parameter, set_the_target_for_exact_parameter, existance_of_user, \
    create_new_userdata, IndividualSchema, update_user_parameter, get_user, show_leaders, check_content

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
        await message.reply("⛔ Отказано в доступе!")

@dp.message_handler(commands=['results'])
async def show_results(message: types.Message):
    """
    This handler will be called when user sends the command '/results' as reply for message
    """
    if await Statistic.get(chat_id=message.chat.id) is not None:
        results = await get_string(chat_id=message.chat.id)
        message_text = f'\n🔶 Общие результаты:\n'
        message_text += f'\n{results}\n'
        await message.reply(f"{message_text}")
    else:
        await bot.send_message(
            chat_id=message.chat.id, text=f'❌ Отсутствуют результаты для группы "{message.chat.full_name}".'
        )

@dp.message_handler(commands=['my_results'])
async def show_results(message: types.Message):
    """
    This handler will be called when user sends the command '/results' as reply for message
    """
    if await existance_of_user(telegram_user_id=message.from_user.id) is not None:
        results = await get_user(telegram_user_id=message.from_user.id)
        message_text = f'🔹 Индивидуальный вклад пользователя @{message.from_user.username} за все время:\n'
        message_text += f'{results}'
        await message.reply(f"{message_text}")
    else:
        await bot.send_message(
            chat_id=message.chat.id, text=f'❌ Отсутствуют результаты для пользователя: @{message.from_user.username}.'
        )

@dp.message_handler(commands=['set_results'])
async def set_results(message: types.Message):
    """
    This handler will be called when the group owner sends the command '/set_results <parameter> <value>'
    """
    # Check if the user is the group owner
    member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status == ChatMemberStatus.OWNER:
        if await Statistic.get(chat_id=message.chat.id) is not None:
            try:
                if len(message.text.split()) <= 3:
                    parameter = int(' '.join(message.text.split()[1:-1]))
                    value = int(message.text.split()[-1])
                    message_text = await set_the_value_for_exact_parameter(chat_id=message.chat.id, param=parameter, value=value)
                else:
                    message_text = '🧐 Я принимаю 2 числа на вход. Первое число - порядковый номер параметра, второе - желаемое значение.'
                await bot.send_message(chat_id=message.chat.id, text=message_text)
            except ValueError:
                await bot.send_message(chat_id=message.chat.id, text='🛑 Неверный формат сообщения для команды.\n Пример: "/set_results 1 5" увеличит параметр "А" до 5')
        else:
            message_text = '📝 Записи в таблице не найдены.'
            await bot.send_message(chat_id=message.chat.id, text=message_text)
    else:
        message_text = "⛔ Отказано в доступе!"
        await bot.send_message(chat_id=message.chat.id, text=message_text)

@dp.message_handler(commands=['set_target'])
async def set_results(message: types.Message):
    """
    This handler will be called when the group owner sends the command '/set_results <parameter> <target_value>'
    """
    member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status == ChatMemberStatus.OWNER:
        if await Statistic.get(chat_id=message.chat.id) is not None:
            try:
                # Get the parameter and value from the command
                if len(message.text.split()) <= 3:
                    parameter = int(' '.join(message.text.split()[1:-1]))
                    target_value = int(message.text.split()[-1])
                    message_text = await set_the_target_for_exact_parameter(chat_id=message.chat.id, param=parameter, target=target_value)
                    await bot.send_message(chat_id=message.chat.id, text=message_text)
                else:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text='🧐 Я принимаю 2 числа на вход. Первое число - порядковый номер параметра, второе - желаемое значение.',
                    )
            except ValueError:
                await bot.send_message(chat_id=message.chat.id, text='🛑 Неверный формат сообщения для команды.\n Пример: "/set_target 1 5" увеличит цель для параметра "А" до 5')
        else:
            message_text = '📝 Записи в таблице не найдены.'
            await bot.send_message(chat_id=message.chat.id, text=message_text)
    else:
        message_text = "⛔ Отказано в доступе!"
        await bot.send_message(chat_id=message.chat.id, text=message_text)

@dp.message_handler(commands=['leaders'])
async def set_results(message: types.Message):
    """
    This handler will be called when the group owner sends the command '/set_results <parameter> <value>'
    """
    # Check if the user is the group owner
    member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status == ChatMemberStatus.OWNER:
        if await check_content(chat_id=message.chat.id) is not None:
            try:
                if len(message.text.split()) <= 2:
                    value = int(message.text.split()[-1])
                    message_text = await show_leaders(qtty=value)
                    await bot.send_message(chat_id=message.chat.id, text=f'Таблица лидеров:\n  \n{message_text}')
                else:
                    message_text = '🧐 Я принимаю только одно число на вход - количество человек в таблице. Пример: "/leaders 10" - выведет таблицу с 10 людьми.'
                    await bot.send_message(chat_id=message.chat.id, text=message_text)
            except ValueError:
                await bot.send_message(chat_id=message.chat.id, text='🛑 Неверный формат сообщения для команды.\n Пример: "/leaders 10" - выведет таблицу с 10 людьми.')
        else:
            message_text = '📝 Записи в таблице не найдены.'
            await bot.send_message(chat_id=message.chat.id, text=message_text)
    else:
        message_text = "⛔ Отказано в доступе!"
        await bot.send_message(chat_id=message.chat.id, text=message_text)

@dp.message_handler(content_types=ContentType.TEXT)
async def handle_text(message: Message):
    text = message.text.lower()
    member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if (
        member.status == ChatMemberStatus.OWNER
        and message.reply_to_message
        and not message.reply_to_message.from_user.is_bot
    ):
        if await Statistic.get(chat_id=message.chat.id) is None:
            await create_new_string(chat_id=message.chat.id, new_db_string=StringSchema(analysis=0, signals=0, screenshot=0, help=0))
        id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username
        if await existance_of_user(telegram_user_id=id) is None:
            await create_new_userdata(telegram_user_id=id, chat_id=message.chat.id, new_db_string=IndividualSchema(username=username, analysis=0, signals=0, screenshot=0, help=0, points=0))
        result = await update_the_value_of_object(chat_id=message.chat.id, text=text)
        message_for_user = await update_user_parameter(telegram_user_id=id, text=text)
        message_text = f'{result}'
        message_text2 = f'{message_for_user}'
        await bot.send_message(chat_id=message.chat.id, text=message_text)
        await bot.send_message(chat_id=message.chat.id, text=message_text2)



async def startup():
    await db.create_all()
    # await dp.start_polling(bot)


if __name__ == '__main__':
    # asyncio.run(startup())
    executor.start_polling(dp, skip_updates=True)

