import asyncio
import os
import logging
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import all_routers

load_dotenv()
TOKEN = os.getenv("TOKEN")
dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=TOKEN)  # type: ignore
    for r in all_routers:  # type: ignore
        dp.include_router(r)
    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
