import logging
import asyncio
import contextlib
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ContentType, ChatMemberStatus
from aiogram.utils import executor
from database import db
from models import Statistic, Individual
from views import StringSchema, IndividualSchema, update_overall_statistic_table, \
    create_chat_entry, set_the_value_for_parameter, set_the_target_for_parameter, \
    create_user_entry, update_individual_statistic_table, increase_and_save, decrease_and_save

TELEGRAM_BOT_TOKEN = '5602947939:AAFMRW-ElOh7FgQFHvmssoSCMtPhu3nm-18'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

load_dotenv()

# Create AsyncEngine & AsyncSession
db.init()

MESSAGE_DISPLAY_TIME = 5
BOT_OWNER = int(os.getenv("BOT_OWNER"))
CHAT_ID = -1001830895816

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when chat owner sends `/help` command
    """
    where_message_sent = message.chat.type
    if message.from_user.id == BOT_OWNER and where_message_sent == 'private':
        await message.reply("Here`s a full list of commands and tips:\n/help - список всех команд, доступных для владельца бота. Работает только в личных сообщениях."
                            "\n/results - Показать общие результаты чата. Работает в чате, может быть вызвана любым пользователем. Вывод удаляется через 15 секунд. "
                            "\n/my_results - Показать вклад одного пользователя. Работает в чате (вывод удаляется через 15 секунд) и в личных сообщениях (вывод не удаляется)."
                            "\n/set_results <parameter_number> <parameter_value> - Задать достигнутое значение для любого параметра. Работает только в личных сообщениях для владельца бота."
                            "\n/set_target <parameter_number> <target_value> - Задать целевое значение для любого параметра. Работает только в личных сообщениях для владельца бота."
                            "\n/leaders <number> - Показать список лидеров по очкам. Длина списка задается числом <number>. Работает в чате и в личных сообщениях."
                            "\n/increase_points_by <value> - Работает только в чате в ответ на сообщение пользователя, которому нужно увеличить очки. "
                            "\n/decrease_points_by <value> - Работает только в чате в ответ на сообщение пользователя, которому нужно уменьшить очки."
                            "\n +`s or -`s - Добавить / убавить достигнутые значения. Работает только в общем чате для владельца бота.")

                        # По царскому велению очки для пользователя -- увеличены на --

@dp.message_handler(commands=['results'])
async def show_results(message: types.Message):
    """
    This handler will be called when any chat user sends the command '/results'.
    """
    if await Statistic.get(chat_id=message.chat.id) is not None:
        results = await Statistic.get(chat_id=message.chat.id)
        message_text = f'\n🔶 Общие результаты:\n'
        message_text += f'\n{results}\n'
        bot_response = await message.reply(f"{message_text}")
    else:
        where_message_sent = message.chat.type
        if where_message_sent != 'private':
            bot_response = await bot.send_message(
                chat_id=message.chat.id, text=f'❌ Отсутствуют результаты для группы "{message.chat.full_name}".'
            )
        else:
            bot_response = await bot.send_message(
                chat_id=message.chat.id,
                text='❌ Используйте эту команду в общем чате!',
            )
    await asyncio.sleep(MESSAGE_DISPLAY_TIME)
    with contextlib.suppress(Exception):
        # Delete the boе response after 5 seconds
        await bot.delete_message(chat_id=bot_response.chat.id, message_id=bot_response.message_id)
        # Delete the command message
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message_handler(commands=['my_results'])
async def show_results(message: types.Message):
    """
    This handler will be called when any chat user sends the command '/my_results'.
    """
    if await Individual.get(telegram_user_id=message.from_user.id) is not None:
        results = await Individual.get(telegram_user_id=message.from_user.id)
        message_text = f'🔹 Индивидуальный вклад пользователя @{message.from_user.username} за все время:\n'
        message_text += f'{results}'
        bot_response = await message.reply(f"{message_text}")
    else:
        bot_response = await bot.send_message(
            chat_id=message.chat.id, text=f'❌ Отсутствуют результаты для пользователя: @{message.from_user.username}.'
        )
    where_message_sent = message.chat.type
    if where_message_sent != 'private':
        await asyncio.sleep(MESSAGE_DISPLAY_TIME)
        with contextlib.suppress(Exception):
        # Delete the bot's response after 5 seconds
            await bot.delete_message(chat_id=bot_response.chat.id, message_id=bot_response.message_id)
        # Delete the command message
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message_handler(commands=['set_results'])
async def set_results(message: types.Message):
    """
    This handler will be called when the bot owner sends the command '/set_results <parameter_number> <parameter_value>' (/set_results 3 10)
    """
    # Check if the user is the bow owner and call a command in private chat
    where_message_sent = message.chat.type
    if message.from_user.id == BOT_OWNER and where_message_sent == 'private':
        if await Statistic.get(chat_id=CHAT_ID) is not None:
            try:
                if len(message.text.split()) <= 3:
                    parameter = int(' '.join(message.text.split()[1:-1]))
                    value = int(message.text.split()[-1])
                    message_text = await set_the_value_for_parameter(chat_id=CHAT_ID, param=parameter, value=value)
                else:
                    message_text = '🧐 Я принимаю 2 числа на вход. Первое число - порядковый номер параметра, второе - желаемое значение.'
                # await bot.send_message(chat_id=CHAT_ID, text=message_text)
                await message.answer(text=message_text)
            except ValueError:
                await message.answer(text='🛑 Неверный формат сообщения для команды.\n Пример: "/set_results 1 5" увеличит параметр "А" до 5')
        else:
            await message.answer(text='📝 Записи в таблице не найдены.')



@dp.message_handler(commands=['set_target'])
async def set_target(message: types.Message):
    """
    This handler will be called when the bot owner sends the command '/set_target <parameter_number> <target_value>' (/set_target 2 40)
    """
    where_message_sent = message.chat.type
    if message.from_user.id == BOT_OWNER and where_message_sent == 'private':
        if await Statistic.get(chat_id=CHAT_ID) is not None:
            try:
                # Get the parameter and value from the command
                if len(message.text.split()) <= 3:
                    parameter = int(' '.join(message.text.split()[1:-1]))
                    target_value = int(message.text.split()[-1])
                    message_text = await set_the_target_for_parameter(chat_id=CHAT_ID, param=parameter, target=target_value)
                    await message.answer(text=message_text)
                else:
                    await message.answer(text='🧐 Я принимаю 2 числа на вход. Первое число - порядковый номер параметра, второе - желаемое значение.',
                    )
            except ValueError:
                await message.answer(text='🛑 Неверный формат сообщения для команды.\n Пример: "/set_target 1 5" увеличит цель для параметра "А" до 5')
        else:
            await message.answer(text='📝 Записи в таблице не найдены.')

@dp.message_handler(commands=['leaders'])
async def show_leaders(message: types.Message):
    """
    This handler will be called when the chat owner sends the command '/leaders <number>' (/leaders 10) which represents top users filtered by earned points.
    """
    # Check if the user is the bot owner
    if message.from_user.id != BOT_OWNER:
        return
    if await Individual.table_content(chat_id=CHAT_ID) is not None:
        try:
            if len(message.text.split()) <= 2:
                value = int(message.text.split()[-1])
                message_text = await Individual.get_top_users_by_points(qtty=value)
                await message.answer(text=f'Таблица лидеров:\n  \n{message_text}')
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            else:
                # await message.answer(text='🧐 Я принимаю только одно число на вход - количество человек в таблице. Пример: "/leaders 10" - выведет таблицу с 10 людьми.')
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except ValueError:
            # await message.answer(text='🛑 Неверный формат сообщения для команды.\n Пример: "/leaders 10" - выведет таблицу с 10 людьми.')
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    else:
        # await message.answer(text='📝 Записи в таблице не найдены.')
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@dp.message_handler(commands=['increase_points_by'])
async def increase_points_by(message: types.Message):
    """
    This handler will be called when the bot owner sends the command '/increase_points_by <number>' (/increase_points_by 10) on reply to the user`s message.
    """
    where_message_sent = message.chat.type
    if message.from_user.id == BOT_OWNER and message.reply_to_message and where_message_sent != 'private':
        try:
            if len(message.text.split()) <= 2:
                user_to_be_awarded = message.reply_to_message.from_user.id
                if await Individual.get(telegram_user_id=user_to_be_awarded) is None:
                    await create_user_entry(telegram_user_id=message.reply_to_message.from_user.id, chat_id=message.chat.id, new_db_string=IndividualSchema(username=message.reply_to_message.from_user.username, analysis=0, signals=0, screenshot=0, help=0, points=0))
                value = int(message.text.split()[-1])
                message_text = await increase_and_save(telegram_user_id=user_to_be_awarded, value=value)
                await message.answer(text=f'{message_text}')
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            else:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            #     await message.answer(text='🧐 Я принимаю только одно число на вход - количество очков для увеличения.')
        except ValueError:
            # await message.answer(text='🛑 Неверный формат сообщения для команды.')
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@dp.message_handler(commands=['decrease_points_by'])
async def increase_points_by(message: types.Message):
    """
    This handler will be called when the bot owner sends the command '/increase_points_by <number>' (/increase_points_by 10) on reply to the user`s message.
    """
    where_message_sent = message.chat.type
    if message.from_user.id == BOT_OWNER and message.reply_to_message and where_message_sent != 'private':
        try:
            if len(message.text.split()) <= 2:
                user_to_be_awarded = message.reply_to_message.from_user.id
                if await Individual.get(telegram_user_id=user_to_be_awarded) is None:
                    await create_user_entry(telegram_user_id=message.reply_to_message.from_user.id, chat_id=message.chat.id, new_db_string=IndividualSchema(username=message.reply_to_message.from_user.username, analysis=0, signals=0, screenshot=0, help=0, points=0))
                value = int(message.text.split()[-1])
                message_text = await decrease_and_save(telegram_user_id=user_to_be_awarded, value=value)
                await message.answer(text=f'{message_text}')
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            else:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            #     await message.answer(text='🧐 Я принимаю только одно число на вход - количество очков для увеличения.')
        except ValueError:
            # await message.answer(text='🛑 Неверный формат сообщения для команды.')
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



@dp.message_handler(content_types=ContentType.TEXT)
async def handle_text(message: Message):
    """
    This handler will be called when the chat owner replies to any user`s message with +`s or -`s'.
    """
    text = message.text.lower()
    if (
        message.from_user.id == BOT_OWNER
        and message.reply_to_message
        and not message.reply_to_message.from_user.is_bot
    ):
        if await Statistic.get(chat_id=message.chat.id) is None:
            await create_chat_entry(chat_id=message.chat.id, new_db_string=StringSchema(analysis=0, signals=0, screenshot=0, help=0))
        if await Individual.get(telegram_user_id=message.reply_to_message.from_user.id) is None:
            await create_user_entry(telegram_user_id=message.reply_to_message.from_user.id, chat_id=message.chat.id, new_db_string=IndividualSchema(username=message.reply_to_message.from_user.username, analysis=0, signals=0, screenshot=0, help=0, points=0))
        message_for_chat = await update_overall_statistic_table(chat_id=message.chat.id, text=text)
        message_for_user = await update_individual_statistic_table(telegram_user_id=message.reply_to_message.from_user.id, text=text)
        first_bot_response = await bot.send_message(chat_id=message.chat.id, text=message_for_chat)
        if message_for_user is not None:
            second_bot_response = await bot.send_message(chat_id=message.chat.id, text=message_for_user)
        await asyncio.sleep(MESSAGE_DISPLAY_TIME)
        with contextlib.suppress(Exception):
        # Delete the bot's response after 5 seconds
            await bot.delete_message(chat_id=first_bot_response.chat.id, message_id=first_bot_response.message_id)
            if message_for_user is not None:
                await bot.delete_message(chat_id=second_bot_response.chat.id, message_id=second_bot_response.message_id)



async def startup():
    await db.create_all()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(startup())
    # executor.start_polling(dp, skip_updates=True)
