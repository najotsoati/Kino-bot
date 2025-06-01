from aiogram import types
from main import dp, bot, ADMIN_ID
import json
import os

# Faylda saqlanadigan kinolar va foydalanuvchilar
MOVIES_FILE = "movies.json"
USERS_FILE = "users.json"

# Yordamchi funksiyalar
def load_movies():
    if not os.path.exists(MOVIES_FILE):
        return {}
    with open(MOVIES_FILE, "r") as f:
        return json.load(f)

def save_movies(movies):
    with open(MOVIES_FILE, "w") as f:
        json.dump(movies, f)

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Kino qo‘shish
@dp.message_handler(lambda msg: msg.from_user.id == ADMIN_ID and msg.text.startswith("/add "))
async def add_movie(msg: types.Message):
    code = msg.text.split(" ")[1]
    if not msg.reply_to_message or not msg.reply_to_message.video:
        await msg.reply("❌ Kino yuklash uchun videoga reply qilib yozing: /add <kod>")
        return
    file_id = msg.reply_to_message.video.file_id
    movies = load_movies()
    movies[code] = file_id
    save_movies(movies)
    await msg.reply(f"✅ Kino kod {code} bilan saqlandi!")

# Statistika
@dp.message_handler(lambda msg: msg.from_user.id == ADMIN_ID and msg.text == "/stats")
async def stats(msg: types.Message):
    users = load_users()
    await msg.reply(f"👥 Umumiy foydalanuvchilar: {len(users)}")

# Xabar yuborish
@dp.message_handler(lambda msg: msg.from_user.id == ADMIN_ID and msg.text.startswith("/send "))
async def broadcast(msg: types.Message):
    text = msg.text.split(" ", 1)[1]
    users = load_users()
    success = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            success += 1
        except:
            pass
    await msg.reply(f"📨 {success} foydalanuvchiga yuborildi.")

# Foydalanuvchilarni avtomatik ro‘yxatga olish
@dp.message_handler()
async def register_users(msg: types.Message):
    users = load_users()
    if msg.from_user.id not in users:
        users.append(msg.from_user.id)
        save_users(users)
      
