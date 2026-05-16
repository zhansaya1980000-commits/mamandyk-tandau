import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiohttp import web

API_TOKEN = '8712387464:AAEVbLaAd5M0TbZOdI45ySWMbZbhEZABa2w'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_scores = {}
# ... (QUESTIONS тізімі бұрынғыдай қалады, код ұзарып кетпес үшін бұл жерге жазбадым, өзіңнің QUESTIONS тізіміңді қалдыр)

# Render-ді алдау үшін кішкентай веб-бет ашу
async def handle(request):
    return web.Response(text="Bot is running!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Тікелей polling-ді фондық режимде қосамыз
    asyncio.create_task(dp.start_polling(bot))
    
    # Render талап ететін веб-портты тыңдаймыз
    app = web.Application()
    app.router.add_get('/', handle)
    
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    # Сервер сөнбеуі үшін шексіз күту режимі
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
