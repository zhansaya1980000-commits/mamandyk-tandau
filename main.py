import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiohttp import web

# СЕНІҢ ТЕЛЕГРАМ БОТ ТОКЕНІҢ
API_TOKEN = '8712387464:AAEVbLaAd5M0TbZOdI45ySWMbZbhEZABa2w'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_scores = {}

QUESTIONS = [
    {"text": "1. Компьютерде код жазу немесе бағдарламаларды зерттеу ұнай ma?", "img": "https://images.unsplash.com/photo-1587620962725-abab7fe55159?q=80&w=500"},
    {"text": "2. Адамдармен тез тіл табысып, олардың психологиясын түсінген қызық па?", "img": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=500"},
    {"text": "3. Сурет салу, дизайн жасау немесе бейнебаян өңдеумен айналысқың келе ме?", "img": "https://images.unsplash.com/photo-1561070791-2526d30994b5?q=80&w=500"},
    {"text": "4. Математикалық есептер шығару және логикалық жұмбақтар шешу оңай ma?", "img": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=500"},
    {"text": "5. Жасанды интеллект, роботтар және жаңа технологиялар әлемі қызықтыра ма?", "img": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=500"}
]

# Render тексеруі үшін кішкентай веб-бет
async def handle(request):
    return web.Response(text="Bot is running completely free!")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_scores[message.from_user.id] = 0
    builder = ReplyKeyboardBuilder()
    builder.button(text="Тестті бастау 🚀")
    await message.answer("✨ Қош келдіңіз! Мамандық анықтау тестін бастау үшін төмендегі батырманы басыңыз.", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "Тестті бастау 🚀")
async def start_survey(message: types.Message):
    await send_question(message, 0)

async def send_question(message: types.Message, q_index: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Иә ✅", callback_data=f"ans_{q_index}_1")
    builder.button(text="Жоқ ❌", callback_data=f"ans_{q_index}_0")
    builder.adjust(2)
    await message.answer_photo(photo=QUESTIONS[q_index]["img"], caption=QUESTIONS[q_index]["text"], reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("ans_"))
async def process_answer(callback: types.CallbackQuery):
    data = callback.data.split("_")
    q_idx, score = int(data[1]), int(data[2])
    uid = callback.from_user.id
    user_scores[uid] = user_scores.get(uid, 0) + score
    
    try:
        await callback.message.delete()
    except:
        pass

    if q_idx + 1 < len(QUESTIONS):
        await send_question(callback.message, q_idx + 1)
    else:
        total = user_scores[uid]
        res = "IT және Жаңа Технологиялар 👨‍💻" if total >= 4 else "Менеджмент және Бизнес 💼" if total >= 2 else "Шығармашылық сала 🎨"
        await callback.message.answer(f"🏁 Тест бітті!\n\nСіздің бағытыңыз: {res}")

async def main():
    # Ботты артқы фонда іске қосу
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(dp.start_polling(bot))
    
    # Render талап ететін веб-сайт бөлігі
    app = web.Application()
    app.router.add_get('/', handle)
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    # Сервердің тоқтап қалмауы үшін шексіз цикл
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
