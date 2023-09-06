from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import *
from functions import FUNCTIONS
import sqlite3
import json
func = FUNCTIONS
connect = sqlite3.connect(name_bd)
cursor = connect.cursor()
bl = []
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_menu(message: types.Message):
    user_id = str(message.from_user.id)
    func.Connect(connect, cursor)
    if func.check_pl(connect, cursor, user_id):
        func.save_info(connect, user_id, "state", "START")
        for_txt = open("img/for.jpg","rb")
        def_txt = open("img/def.jpg","rb")
        while_txt = open("img/while.jpg","rb")
        read_file_txt = open("img/read_file.jpg","rb")
        await message.answer(f"{instruckt}\n\nПримеры написание кода:", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_photo(chat_id=message.chat.id,photo=for_txt)
        await bot.send_photo(chat_id=message.chat.id,photo=def_txt)
        await bot.send_photo(chat_id=message.chat.id,photo=while_txt)
        await bot.send_photo(chat_id=message.chat.id,photo=read_file_txt)
    else:
        await message.answer("Если хотите прочитать инструкцию, введите команду /manual.", reply_markup=types.ReplyKeyboardRemove())
        func.save_info(connect, user_id, "state", "START")


@dp.message_handler(commands=['manual'])
async def manual(message: types.Message):
    for_txt = open("img/for.jpg", "rb")
    def_txt = open("img/def.jpg", "rb")
    while_txt = open("img/while.jpg", "rb")
    read_file_txt = open("img/read_file.jpg", "rb")
    await message.answer(f"{instruckt}\n\nПримеры написание кода:")
    await bot.send_photo(chat_id=message.chat.id, photo=for_txt)
    await bot.send_photo(chat_id=message.chat.id, photo=def_txt)
    await bot.send_photo(chat_id=message.chat.id, photo=while_txt)
    await bot.send_photo(chat_id=message.chat.id, photo=read_file_txt)

@dp.message_handler(commands=['compel'])
async def comp(message: types.Message):
    user_id = str(message.from_user.id)
    func.save_info(connect, user_id, "state", "COMPEL")
    func_dict = func.conv_str_dc(func.get_variable(connect, user_id, "func"))
    com = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in func_dict.keys():
        com.add(i)
    await message.answer("Напишите свой код.", reply_markup=com)



@dp.message_handler(commands=['comands'])
async def comand(message: types.Message):
    user_id = str(message.from_user.id)
    func.save_info(connect, user_id, "state", "ADDCOMAND")
    await message.answer("Напишите название функции, которую хотите сохранить.\nЕсли хотите поменять содержание функции напишите уже имеющиеся название.")


@dp.message_handler(commands=['set_info'])
async def set_info_fil(message: types.Message):
    user_id = str(message.from_user.id)
    func.save_info(connect, user_id, "state", "SET_INFO")
    await message.answer("Напишите данные с которыми планируете работать.")

@dp.message_handler(commands=['rem_com'])
async def remove_command(message: types.Message):
    user_id = str(message.from_user.id)
    func.save_info(connect, user_id, "state", "REM_COM")
    func_dict = func.conv_str_dc(func.get_variable(connect, user_id, "func"))
    com = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in func_dict.keys():
        com.add(i)
    await message.answer("Отправьте функцию которую хотели бы удалить.",reply_markup=com)

@dp.message_handler()
async def main(message: types.Message):

    user_id = str(message.from_user.id)
    if message.text and func.get_variable(connect, user_id, "state") == "ADDCOMAND":
        func_dict = func.conv_str_dc(func.get_variable(connect, user_id, "func"))
        if message.text not in list(func_dict.keys()):
            await message.answer("Напишие функцию.")
            func.save_info(connect, user_id, "name_func", message.text)
            func.save_info(connect, user_id, "state", "ADD_FUNC")
        else:
            await message.answer(f'Функция с таким названием уже есть, хотите поменять ее содержание?\n\nСама функция:\n{func_dict[message.text]}', reply_markup=choice_kb)
            func.save_info(connect, user_id, "state", "CHOICE_FN")
            func.save_info(connect, user_id, "name_func", message.text)

    if message.text != func.get_variable(connect, user_id, "name_func") and func.get_variable(connect, user_id, "state") == "ADD_FUNC":
        func_dict = func.conv_str_dc(func.get_variable(connect, user_id, "func"))
        func_dict[func.get_variable(connect, user_id, "name_func")] = '\n'.join(message.text.split("\n"))
        func.save_info(connect, user_id, "func", func.conv_dc_str(func_dict).replace("\"","\'"))
        await message.answer(f"Функция \"{func.get_variable(connect, user_id, 'name_func')}\" сохранена.\nХотите продолжить добавление функций?", reply_markup=choice_kb)
        func.save_info(connect, user_id, "state", "CHOICE_END_FN")

    if message.text == "Да":
        if func.get_variable(connect, user_id, "state") == "CHOICE_END_FN":
            await message.answer("Напишите название функции.", reply_markup=types.ReplyKeyboardRemove())
            func.save_info(connect, user_id, "state", "ADDCOMAND")
        if func.get_variable(connect, user_id, "state") == "CHOICE_FN":
            await message.answer("Напишите функцию")
            func.save_info(connect, user_id, "state", "ADD_FUNC")

    if message.text == "Нет":
        if func.get_variable(connect, user_id, "state") == "CHOICE_END_FN":
            await message.answer("Выберите действие нажав на кнопку 'меню'.", reply_markup=types.ReplyKeyboardRemove())
            func.save_info(connect, user_id, "state","START")
        if func.get_variable(connect, user_id, "state") == "CHOICE_FN":
            await message.answer("Напишите название функции.",reply_markup=types.ReplyKeyboardRemove())
            func.save_info(connect, user_id, "state", "ADDCOMAND")

    if func.get_variable(connect, user_id, "state") == "COMPEL":
        if message.text in func.conv_str_dc(func.get_variable(connect, user_id, "func")).keys():
            func_ = "\n".join(func.conv_str_dc(func.get_variable(connect, user_id, "func"))[message.text].split("\\n"))
            await message.answer(func_[:-1])
        else:
            code = "import itertools\n"+message.text.replace("print", "new_peremennayi_blin =")
            if "read_file" in code:
                file = str(open(f"files/{user_id}","rb").read())[1:].replace(r"\r", "")
                code = code.replace("read_file", file)
            try:
                a, b = {}, {}
                exec(code, a, b)
                await message.answer(str(list(b.values())[-1]))
                if "new_peremennayi_blin =" in code:
                    if len(str(list(b.values())[-1])) > 1000:
                        await message.answer("Файл слишком большой чтобы его отправить целиком.")
                        await message.answer(f"{str(list(b.values())[-1][1:900])}...")
                    else:
                        await message.answer(str(list(b.values())[-1]))
                else:
                    await message.answer("Вы не написали print.")
            except:
                try:
                    a, b, = {},{}
                    exec(code,b)
                    await message.answer(str(list(b.values())[-1]))
                except:
                    await message.answer("В коде ошибка!")

    if message.text and func.get_variable(connect, user_id, "state") == "SET_INFO":
        open(f"files/{user_id}","w").write(message.text)
        await message.answer("Данные успешно сохранены.")
        func.save_info(connect, user_id, "state", "START")

    if func.get_variable(connect,user_id, "state") == "REM_COM" and message.text in list(func.conv_str_dc(func.get_variable(connect, user_id, "func")).keys()):
        func_ls = list(filter(lambda x: message.text not in x,list(func.conv_str_dc(func.get_variable(connect, user_id, "func")).items())))
        new_func_dc = {}
        for i in func_ls:
            new_func_dc[i[0]] = i[1]
        func.save_info(connect, user_id, "func", func.conv_dc_str(new_func_dc).replace("\"","\'"))
        await message.answer(f"Функция \"{message.text}\" успешно удалена.", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Для продолжения нажмите на кнопку 'меню' и выберите команду.")

@dp.message_handler(content_types=['document'])
async def scan_message(message: types.Message):
    if func.get_variable(connect, str(message.from_user.id), "state") == "SET_INFO":
        await message.document.download("files/" + str(message.from_user.id))
        await message.answer("Данные успешно сохранены")
        func.save_info(connect, str(message.from_user.id), "state", "START")

executor.start_polling(dp)