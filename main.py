from aiogram import Bot, Dispatcher, executor, types
import logging
import json
import os

API_TOKEN = '6820687034:AAGQZZdavImQEkbyi6B5SvH1zyW0Bw3y1g8'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Fayl nomlari
MOVIES_FILE = "movies.json"
USERS_FILE = "users.json"

# Majburiy obuna kanali
CHANNEL_USERNAME = "@NajotSoati"

# Foydalanuvchini majburiy obunaga tekshirish
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

# /start buyrug‘i
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    subscribed = await check_subscription(user_id)

    if not subscribed:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔗 Obuna bo‘lish", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}"))
        await message.answer("❗ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=markup)
        return

    await message.answer("🎬 Kodni kiriting (masalan: 1, 2, 3...)")

    # Foydalanuvchini saqlash
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    else:
        users = []

    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

# Kod bo‘yicha kinoni yuborish
@dp.message_handler(lambda msg: msg.text.isdigit())
async def send_movie(message: types.Message):
    code = message.text.strip()
    user_id = message.from_user.id

    if not await check_subscription(user_id):
        await message.answer("❗ Avval kanalga obuna bo‘ling!")
        return

    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, "r") as f:
            movies = json.load(f)
    else:
        movies = {}

    if code in movies:
        await message.answer_video(movies[code], caption=f"🎬 Kod: {code}")
    else:
        await message.answer("❌ Bunday kodga mos kino topilmadi.")

# Fayllar mavjud bo‘lmasa — yaratib qo‘yish
if not os.path.exists(MOVIES_FILE):
    with open(MOVIES_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

# Admin panelni import qilish
import admin

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
    
