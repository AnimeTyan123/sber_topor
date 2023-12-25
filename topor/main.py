from secret import token
from pyrogram.client import Client
from pyrogram.enums import ChatAction
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton as Ikb,
    InlineKeyboardMarkup as Ikm,
    InlineQueryResultArticle,
    InputTextMessageContent,
    CallbackQuery,
    InlineQuery,
    Message,
)
import asyncio

app = Client(
    name="sbertopor",
    api_id="1",
    api_hash="b6b154c3707471f5339bd661645ed3d6",
    bot_token=token,
)

# List of trigger phrases
responses = [
    "Оформляю подписку Cберпрайⷨ ...",
    "🪓",
    "🪓🪓",
    "🪓🪓🪓",
    "🪓🪓🪓🪓",
    "Топор был выкурен! 🚬",
]
triggers = ['кури', 'топор']

# Global counter variable
click_count = 0

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Привет! Саси")

@app.on_message(filters.text)
async def emoji_sender(client, msg: Message):
    if msg.via_bot:
        return
    for trigger in triggers:
        if trigger in msg.text.lower():
            await smoke_axe(msg)
            return

@app.on_inline_query()
async def handle_inline_query(client, inline: InlineQuery):
    # Create separate "smoke" and "statistics" buttons
    smoke_button = Ikb("Покурить топор", "smoke")
    statistics_button = Ikb("Статистика", "statistics")

    # Create an inline keyboard with both buttons
    inline_keyboard = Ikm([[smoke_button, statistics_button]])

    await inline.answer(
        results=[
            InlineQueryResultArticle(
                title='Покурить топор',
                input_message_content=InputTextMessageContent(
                    'Нажми кнопку ниже, чтобы покурить топор',
                ),
                reply_markup=inline_keyboard,
                thumb_url='https://i.postimg.cc/4dm21qbz/IMG-20231215-115344-720.jpg',
            ),
        ],
        is_personal=True,
        cache_time=0,
    )
    await asyncio.sleep(1)

@app.on_callback_query()
async def answer(client, cb: CallbackQuery):
    global click_count  # Access the global counter variable

    if cb.data == "smoke":
        await cb.answer('Начинаем процесс курения...')
        for response in responses:
            await asyncio.sleep(1)
            await cb.edit_message_text(response)
    elif cb.data == "statistics":
        # Increment and display the click count
        click_count += 1
        await cb.answer(f'Вы нажали кнопку "Покурить топор" {click_count} раз.')
        

async def smoke_axe(msg: Message):
    sent_message = None
    for response in responses:
        if sent_message:
            await msg.reply_chat_action(ChatAction.TYPING)
            await asyncio.sleep(1)
            await sent_message.delete()
        sent_message = await msg.reply(response)

app.run()
