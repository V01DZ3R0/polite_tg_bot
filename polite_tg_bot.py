from pyrogram import Client, filters
import asyncio
from datetime import datetime, timedelta
from pyrogram.types import ChatPermissions


api_id=input("Введите api_id: ")
api_hash=input("Введите api_hash: ")
app = Client("my_bot", api_id, api_hash)

# Список нецензурных слов для примера
bad_words = ["хуй","блять","пизда","сука","ебать","нецензурное_слово"]

# Хранение информации о пользователях
user_data = {}

@app.on_message(filters.text & ~filters.private)
async def check_message(client, message):
    user_id = message.from_user.id
    text = message.text.lower()
    time = message.date
    bad_words_count = sum(word in text for word in bad_words)

    if user_id not in user_data:
        user_data[user_id] = {"count": 0, "last_check": 0}

    user_data[user_id]["count"] += bad_words_count

    if user_data[user_id]["count"] >= 5:
        now = datetime.now()
        until_date = now + timedelta(days=0.5)

        # Создаем объект ChatPermissions с нужными правами
        permissions = ChatPermissions(can_send_messages=False)

        # Предполагаем, что client и message уже определены
        await client.restrict_chat_member(message.chat.id, user_id, permissions, until_date)
        user_data[user_id]["count"] = 0
        await message.reply("Вы были ограничены в доступе к чату на 12 часов за чрезмерное использование нецензурной лексики.")
app.run()
