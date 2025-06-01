from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging, os, asyncio

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

movies = {
    "1": "https://t.me/mutfilmllar/140?single"
}

async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    if not await check_subscription(message.from_user.id):
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"),
            InlineKeyboardButton("✅ Tekshirish", callback_data="check_subs")
        )
        await message.answer("Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=markup)
        return
    await message.answer("Salom! Kodni kiriting (masalan: 1):")

@dp.callback_query_handler(lambda c: c.data == "check_subs")
async def check_callback(callback_query: types.CallbackQuery):
    if await check_subscription(callback_query.from_user.id):
        await callback_query.message.edit_text("✅ Obuna bo‘lganingiz tasdiqlandi!\nEndi kod kiriting:")
    else:
        await callback_query.answer("Hali obuna emassiz!", show_alert=True)

@dp.message_handler()
async def send_movie(message: types.Message):
    code = message.text.strip()
    if code in movies:
        await message.answer_video(movies[code])
    else:
        await message.answer("❌ Bunday kod topilmadi.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
  
