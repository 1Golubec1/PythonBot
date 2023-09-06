from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
TOKEN = "6204040336:AAGzvROAbARWYE1N_12C4HPS6Zc75z-k9IA"
python_bot = "6204040336:AAGzvROAbARWYE1N_12C4HPS6Zc75z-k9IA"
test_python_bot = "6027106205:AAHrklemczcyOjL_ueHgK8_nVC_UtKDjfIM"
name_bd = "interpritator_python"
instruckt = open("instruckt.txt", "r", encoding="UTF-8").read()

yes_bt = KeyboardButton("Да")
no_bt = KeyboardButton("Нет")

choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
choice_kb.add(yes_bt, no_bt)