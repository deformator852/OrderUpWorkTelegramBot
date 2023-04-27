import os
from PIL import Image,ImageOps
import all_download
from create_bot import *
from aiogram import types
from keyboards.keyboard import kb_bot,kb_choice
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from datetime import datetime
from aiogram.types import CallbackQuery
import imagehash
import asyncio

class FSMGetId(StatesGroup):
    hash_first_image = State()
    hash_second_image = State()
async def change_photo(path_to_first_image,path_to_second_image):
    image1 = Image.open(path_to_first_image)
    image2 = Image.open(path_to_second_image)
    width1, height1 = image1.size
    width2, height2 = image2.size
    square_size = max(width1, height1, width2, height2)
    min_width = 640
    min_height = 480
    max_width = 1980
    max_height = 1048
    if square_size < min_width or square_size < min_height:
        square_size = max(min_width, min_height)
    if square_size > max_width or square_size > max_height:
        square_size = min(max_width, max_height)
    image1 = ImageOps.pad(image1.crop((0, 0, width1, height1)), (square_size, square_size))
    image2 = ImageOps.pad(image2.crop((0, 0, width2, height2)), (square_size, square_size))
    new_width = square_size * 2
    new_height = square_size
    if new_width < min_width or new_height < min_height:
        new_width = max(min_width, min_height * 2)
        new_height = max(min_height, int(new_width / 2))
    if new_width > max_width or new_height > max_height:
        new_width = min(max_width, int(max_height * 2))
        new_height = min(max_height, int(new_width / 2))

    new_image = Image.new('RGB', (new_width, new_height))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (square_size, 0))
    new_image.save("merged_image.jpg")
    # await FSMGetId.next()
async def command_start(mesasge: types.Message,state: FSMContext):
    await FSMGetId.hash_first_image.set()
    await bot.send_message(mesasge.chat.id,"Bot started!",reply_markup=kb_bot)
    await FSMGetId.next()

async def command_take_photos(message: types.Message,state:FSMContext):
    images = os.listdir("images")
    await change_photo("images/" + images[0],"images/"+ images[1])
    await bot.send_photo(message.chat.id,types.InputFile("merged_image.jpg"),reply_markup=kb_choice)
    async with state.proxy() as data:
        with Image.open('images/'+images[0]) as first_image:
            hash_first = imagehash.average_hash(first_image)
        with Image.open('images/'+images[1]) as second_image:
            hash_second = imagehash.average_hash(second_image)
        data["hash_first_image"] = hash_first
        data["hash_second_image"] = hash_second
    await bot.send_message(message.chat.id,"Hash first image: " +str(hash_first))
    await bot.send_message(message.chat.id,"Hash second image: " + str(hash_second))
    await FSMGetId.next()



async def command_download_all_data(message: types.Message):
    await all_download.all_download()

@dp.callback_query_handler(text='command_first',state=FSMGetId)
async def first_photo_callback(callback: CallbackQuery,state: FSMContext):
    message = callback.message
    current_date = datetime.now()
    current_date = str(current_date.year) + "-" + str(current_date.month) + "-" + str(current_date.day) + " " + str(
        current_date.hour) + ":" + str(current_date.minute)
    async with state.proxy() as data:
        message_json = {"messasge_id": message.message_id, "date": current_date,
                        "platform": "telegram",
                        "first_name": message.from_user.first_name,
                        "lastname": message.from_user.last_name,
                        "hash_first_image": str(data["hash_first_image"]),
                        "hash_second_image": str(data["hash_second_image"]),
                        "hash_selected_message": str(data["hash_first_image"])}
    await bot.send_message(chat_id="", text=message_json)
    #chat_id = Channel for data
    await state.finish()
@dp.callback_query_handler(text='command_second',state=FSMGetId)
async def second_photo_callback(callback: CallbackQuery,state: FSMContext):
    message = callback.message
    current_date = datetime.now()
    current_date = str(current_date.year) + "-" + str(current_date.month) + "-" + str(current_date.day) + " " + str(
        current_date.hour) + ":" + str(current_date.minute)
    async with state.proxy() as data:
        message_json = {"messasge_id": message.message_id,
                        "date": current_date,
                        "platform": "telegram",
                        "first_name": message.from_user.first_name,
                        "lastname": message.from_user.last_name,
                        "hash_first_image": str(data["hash_first_image"]),
                        "hash_second_image": str(data["hash_second_image"]),
                        "hash_selected_message": str(data["hash_second_image"])}
    await bot.send_message(chat_id="", text=message_json)
    # chat_id = Channel for data
    await state.finish()

def register_callback_query_handlers():
    dp.callback_query_handler(first_photo_callback,text="command_first")
    dp.callback_query_handler(second_photo_callback,text="command_second")
def register_bot_handlers():
    dp.register_message_handler(command_take_photos,commands="take_photos")
    dp.register_message_handler(command_start,commands="start")
    dp.register_message_handler(command_download_all_data,commands="download_all_data")

