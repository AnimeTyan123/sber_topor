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
import psutil
import datetime

app = Client(
    name="sbertopor",
    api_id="1",
    api_hash="b6b154c3707471f5339bd661645ed3d6",
    bot_token=token,
)

smoke_count = 0
responses_ru = [
    "Оформляю подписку Сберпрайм...",
    "🪓",
    "🪓🪓",
    "🪓🪓🪓",
    "🪓🪓🪓🪓",
    "Топор был выкурен! 🚬",
]
responses_en = [
    "Subscribing to Sberprime..."
    "🪓",
    "🪓🪓",
    "🪓🪓🪓",
    "🪓🪓🪓🪓",
    "Axe was smoked! 🚬",
]
responses_uk = [
    "Виконую пошук нахрюків..."
    "🐖",
    "🐖🪓",
    "🐖🪓🔥",
    "🐖🪓🔥🥩",
    "Нахрюк прокоптився! 🐖➡️🥩",
]

@app.on_message(filters.command("start"))
async def start(
    client,
    msg: Message,
):
    lang = msg.from_user.language_code
    match lang:
        case 'ru':
            await msg.reply("Привет! Саси")
        case 'uk':
            await msg.reply("Привіт! Сосі")
        case 'en':
            await msg.reply("Hello! Suck my dick")


@app.on_message(filters.command("status"))
async def status(client, message):
    cpu_load = psutil.cpu_percent()
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    cpu_temp = psutil.sensors_temperatures().get('coretemp', [None])[0]
    if cpu_temp:
        cpu_temp = cpu_temp.current
    else:
        cpu_temp = 'N/A'
    ram = psutil.virtual_memory()
    ram_used = ram.used // (1024 ** 2)
    ram_total = ram.total // (1024 ** 2)
    uptime_str = str(uptime).split('.')[0]
    status_message = (
        f"🖥 cpu load: {cpu_load}%",
        f"🧠 ram: {ram_used} mib / {ram_total} mib",
        f"⏱ uptime: {uptime_str}",
        f"🌡 cpu temp: {cpu_temp}° c",
    )
    await message.reply_text("\n".join(status_message))


@app.on_message(filters.text)
async def emoji_sender(
    client,
    msg: Message,
):
    triggers_ru = ['кури', 'топор']
    triggers_en = ['smoke', 'axe']
    triggers_uk = ['курi', 'курi']
    if msg.via_bot:
        return
    for trigger in triggers_ru:
        if trigger in msg.text.lower():
            await smoke_axe(msg, responses_ru)
            return
    for trigger in triggers_en:
        if trigger in msg.text.lower():
            await smoke_axe(msg, responses_en)
            return
        for trigger in triggers_uk:
            if trigger in msg.text.lower():
                await smoke_axe(msg, responses_uk)
            return

@app.on_inline_query()
async def handle_inline_query(client, inline: InlineQuery):
    print(inline.from_user.language_code)
    lang = inline.from_user.language_code
    match lang:
        case 'ru':
            title = "Покурить топор"
            smoke_text = 'Нажми кнопку ниже, чтобы покурить топор'
            statistics_text = "Статистика"
        case 'uk':
            title = "здобути перемогу"
            smoke_text = 'Натисніть кнопку нижче, щоб покурити сокиру'
            statistics_text = "Статистика"
        case _:
            title = "Smoke axe"
            smoke_text = 'Press button below to smoke axe'
            statistics_text = "Stats"

    # Переместите определение кнопок за пределы условного оператора
    smoke_button = Ikb(title, "smoke")
    statistics_button = Ikb(statistics_text, "statistics")

    inline_keyboard = Ikm([[smoke_button, statistics_button]])

    await inline.answer(
        results=[
            InlineQueryResultArticle(
                title=title,
                input_message_content=InputTextMessageContent(
                    smoke_text,
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
    global smoke_count
    lang = cb.from_user.language_code
    match lang:
        case 'uk':
            start_smoking = "Розгортаємо швайнолокатори..."
            responses = responses_uk
        case 'ru':
            start_smoking = "Начинаем процесс курения..."
            responses = responses_ru
        case _:
            start_smoking = "Starting process of smoking..."
            responses = responses_en
    if cb.data == "smoke":
        smoke_count += 1
        await cb.answer(start_smoking)
        for response in responses:
            await asyncio.sleep(1)
            await cb.edit_message_text(response)
    elif cb.data == "statistics":
        # Increment and display the click count
        await cb.answer(f'Вы нажали кнопку "Покурить топор" {smoke_count} раз.')
        

async def smoke_axe(
    msg: Message,
    responses: list[str]
):
    global smoke_count
    smoke_count += 1
    sent_message = None
    for response in responses:
        if sent_message:
            await msg.reply_chat_action(ChatAction.TYPING)
            await asyncio.sleep(1)
            sent_message = await sent_message.edit_text(response)
        else:
            sent_message = await msg.reply(response)

app.run()
