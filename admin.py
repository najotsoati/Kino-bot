from aiogram import types
from main import dp, bot, MOVIES_FILE, USERS_FILE, CHANNEL_USERNAME
import json
import os

# Admin ID (o'zingizning Telegram ID raqamingiz)
ADMIN_ID = 6359279097  # @InomovB uchun

# Kino yuklash va kod berish
@dp.message_handler(content_types=['video'], user_id=ADMIN_ID)
async def add_movie(message: types.Message):
    await message.answer("🎬 Kino yuklandi.\nIltimos, ushbu kino uchun kod yuboring:")

    # Kino fayl ID sini vaqtincha saqlaymiz
    with open("temp_video.txt", "w") as f:
        f.write(message.video.file_id)

@dp.message_handler(lambda msg: msg.text.isdigit(), user_id=ADMIN_ID)
async def save_code(message: types.Message):
    if os.path.exists("temp_video.txt"):
        with open("temp_video.txt", "r") as f:
            file_id = f.read()

        code = message.text.strip()

        # Kino faylini bazaga yozish
        if os.path.exists(MOVIES_FILE):
            with open(MOVIES_FILE, "r") as f:
                movies = json.load(f)
        else:
            movies = {}

        movies[code] = file_id

        with open(MOVIES_FILE, "w") as f:
            json.dump(movies, f)

        await message.answer(f"✅ Kino {code}-kod bilan saqlandi.")
        os.remove("temp_video.txt")
    else:
        await message.answer("⚠ Avval kino yuboring!")

# Statistika
@dp.message_handler(commands=["stat"], user_id=ADMIN_ID)
async def show_stats(message: types.Message):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        total = len(users)
    else:
        total = 0
    await message.answer(f"📊 Foydalanuvchilar soni: {total} ta")

# Obunachilar ro'yxati
@dp.message_handler(commands=["users"], user_id=ADMIN_ID)
async def list_users(message: types.Message):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        txt = "\n".join([str(u) for u in users])
        await message.answer(f"📄 Foydalanuvchilar:\n{txt}")
    else:
        await message.answer("Foydalanuvchilar yo‘q")

# Xabar yuborish (broadcast)
@dp.message_handler(commands=["send"], user_id=ADMIN_ID)
async def broadcast(message: types.Message):
    msg = message.text.split(" ", 1)
    if len(msg) < 2:
        await message.answer("✍ /send [xabar] shaklida yozing")
        return
    text = msg[1]

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    count = 0
    for user in users:
        try:
            await bot.send_message(user, text)
            count += 1
        except:
            continue
    await message.answer(f"📤 {count} ta foydalanuvchiga yuborildi")

# User ID orqali topish
@dp.message_handler(commands=["find"], user_id=ADMIN_ID)
async def find_user(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("🔍 /find [user_id] deb yozing")
        return
    uid = int(args[1])

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    else:
        users = []

    if uid in users:
        await message.answer(f"✅ {uid} botdan foydalanmoqda.")
    else:
        await message.answer(f"❌ {uid} topilmadi.")

# Kanalni yangilash
@dp.message_handler(commands=["setchannel"], user_id=ADMIN_ID)
async def set_channel(message: types.Message):
    global CHANNEL_USERNAME
    args = message.text.split()
    if len(args) < 2:
        await message.answer("ℹ Foydalanish: /setchannel @kanal_nomi")
        return
    CHANNEL_USERNAME = args[1]
    await message.answer(f"✅ Kanal yangilandi: {CHANNEL_USERNAME}")
    
