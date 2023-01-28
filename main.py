from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram .types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import config 
import logging
import os
import sqlite3

bot = Bot(config.token)
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

connect = sqlite3.connect('users.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    username VARCHAR(255),
    id_user INTEGER,
    phone_number INTEGER
    );
    """)
connect.commit()

connect = sqlite3.connect('address.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS address (
    id_user INTEGER,
    address_longitude VARCHAR(255),
    address_latitude VARCHAR(255)
    );
    """)
connect.commit()

connect = sqlite3.connect('orders.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
    title TEXT,
    address_destination VARCHAR(255),
    date_time_order VARCHAR(255)
    );
    """)
connect.commit()

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(msg:types.Message):
    await msg.reply("OK")
    print(msg.contact['phone_number'])
    
@dp.message_handler(content_types=types.ContentType.LOCATION)
async def get_contact(msg:types.Message):
    await msg.reply("OK")
    print(msg.location)
    await bot.send_location(msg.chat.id, msg.location['latitude'], msg.location['longitude'])

@dp.message_handler(commands= ['start'])
async def on_start(message: types.Message):
    
    inline_kb= [
        InlineKeyboardButton('Отправить номер', callback_data=" contact"),
        InlineKeyboardButton('Отправить локацию', callback_data="location"),
        InlineKeyboardButton('Заказать еду', callback_data="zakaz"),
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_kb)
    await message.answer("Спосиба  заказ", reply_markup=inline_keyboard)

    cursor = connect.cursor()
    cursor.execute(f"SELECT id_user FROM users WHERE id_user = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"""INSERT INTO users VALUES ('{message.from_user.username}', 
                        '{message.from_user.first_name}', '{message.from_user.last_name}', 
                        {message.from_user.id}, {message.phone_number})""")
    connect.commit()
    
       
executor.start_polling(dp)
    
    
    
    
    
    
    
    
    
    
   