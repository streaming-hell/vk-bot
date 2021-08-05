import asyncio
import logging
import handlers
from bot import bot


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await bot.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
