import asyncio
from aiogram import Bot, Dispatcher
from config import get_config
from handlers import setup_handlers
from clients import setup_clients
from middlewares import setup_middlewares
import logging

logging.basicConfig(level=logging.INFO)


bot = Bot(token=get_config().TRAINING_BOT_TOKEN)


async def main():
    print("Бот запущен!")
    dp = Dispatcher()

    setup_handlers(dp)
    setup_clients(dp)
    setup_middlewares(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
