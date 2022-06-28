from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('Главное меню')

# --- Main Menu ---
# btnRandom = KeyboardButton('Погода')
btnOther = KeyboardButton('Прочее')  # подменю
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnOther)

# --- Other menu ---
btnInfo = KeyboardButton('Информация')
btnMoney = KeyboardButton('Курс валют')
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnMoney, btnMain)
