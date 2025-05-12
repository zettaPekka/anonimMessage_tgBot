import asyncio
from aiogram import Dispatcher

import logging

from core.init_bot import bot
from handlers.user_handlers import user_router
from handlers.admin_handlers import admin_router
from database.init_db import init_database


logging.basicConfig(level=logging.INFO)

async def main() -> None:
    await init_database()
    await bot.delete_webhook(drop_pending_updates=True)
    
    dp = Dispatcher()
    dp.include_routers(admin_router, user_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        pass