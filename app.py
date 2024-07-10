import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from handlers.payment import pay_route
from common.bot_cmds_lst import private

logging.basicConfig(level=logging.INFO)

ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(pay_route)

async def main():
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

asyncio.run(main())