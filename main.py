import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from handlers import basicHandlers, onchainHandlers
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('TOKEN'), parse_mode="HTML")
dp = Dispatcher()

async def main():
    dp.include_routers(basicHandlers.router, onchainHandlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

@dp.message(Command('start'))
async def start(message: Message):
    photo = FSInputFile('pics/helloPic.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Привет! Я бот, который может выполнить <b>множество</b> команд в разных блокчейнах.\n\nДля просмотра списка"
                                                                       "команд воспользуйся <code>/help</code>. Начни с выбора блокчейна, для этого воспользуйся командой <code>/choosechain</code>. Сейчас ты находишься в сети <b>BSC</b>.")

if __name__ == '__main__':
    asyncio.run(main())