import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData

API_TOKEN = "8535761650:AAGAhgUmEh771S68kHUx6dgsBG2Iz9bTxIA"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ================= CALLBACK =================
class QuizCallback(CallbackData, prefix="quiz"):
    answer: str

# ================= START =================
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привіт! Я твій бот \nНапиши /menu")

# ================= HELP =================
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "/start - запуск\n"
        "/menu - меню\n"
        "/quiz - вікторина\n"
        "/about - про мене\n"
        "/version - версія\n"
        "/facts - випадковий факт"
    )

# ================= ABOUT =================
@dp.message(Command("about"))
async def about_command(message: Message):
    await message.answer("Я створений Полінкою💖(Але якщо чесно…більшість роботи зробив чат GPT)")

# ================= VERSION =================
@dp.message(Command("version"))
async def version_command(message: Message):
    await message.answer("Версія бота: 2.0 ")

# ================= MENU =================
@dp.message(Command("menu"))
async def menu(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Цікавий факт 💡")],
            [KeyboardButton(text="Мій розклад 📅")],
            [KeyboardButton(text="Налаштування ⚙️")],
        ],
        resize_keyboard=True
    )
    await message.answer("Обери опцію👇", reply_markup=keyboard)

# ================= QUIZ =================
@dp.message(Command("quiz"))
async def quiz(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="9 березня", callback_data=QuizCallback(answer="correct").pack())],
            [InlineKeyboardButton(text="10 березня", callback_data=QuizCallback(answer="wrong").pack())],
        ]
    )
    await message.answer("Коли народився Тарас Шевченко?", reply_markup=keyboard)

# ================= QUIZ ANSWER =================
@dp.callback_query(QuizCallback.filter())
async def quiz_answer(callback: CallbackQuery, callback_data: QuizCallback):
    if callback_data.answer == "correct":
        await callback.message.answer("Правильно! ✅")
    else:
        await callback.message.answer("Спробуй ще раз! ❌")
    await callback.answer()

# ================= TEXT =================
facts = [
    "24 серпня 1991 — Незалежність України 🇺🇦",
    "Київ — столиця України 🏙️",
    "Найбільша річка — Дніпро 🌊"
]

@dp.message()
async def text_handler(message: Message):
    text = message.text.lower()

    if "привіт" in text:
        await message.answer(f"Привіт, {message.from_user.first_name}! 😊")

    elif "цікавий факт" in text:
        await message.answer(random.choice(facts))

    elif "мій розклад" in text:
        await message.answer("Для тебе завжди вільний 😎")

    elif "налаштування" in text:
        await message.answer("Тут поки нічого нема ⚙️")

    elif "історія" in text:
        await message.answer(random.choice(facts))

    elif "дякую" in text:
        await message.answer("Завжди радий допомогти 😊")

    else:
        # Захист від дурня
        await message.answer("Я не розумію 😢\nСпробуй /menu або /help")

# ================= FACTS COMMAND =================
@dp.message(Command("facts"))
async def facts_command(message: Message):
    await message.answer(random.choice(facts))

# ================= RUN =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())