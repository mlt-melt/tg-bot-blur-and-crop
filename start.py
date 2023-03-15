import os
import time
from config import dp, bot
from croper import croper
from aiogram import types
import os
import random
import requests
import mode


@dp.message_handler(commands='start')
async def startcmd(message: types.Message):
    mode.change_mode(message.from_user.id, "original")
    await message.answer(f"Добро пожаловать. Это бот для преобразования картинок. Вы можете прислать мне фото или ссылку на него\n\nВаш режим - оригинальный размер\nДля изменения режима введите команду '/mode'", parse_mode="html")

@dp.message_handler(commands='mode')
async def startcmd(message: types.Message):
    userMode = mode.check(message.from_user.id)
    if userMode == "original":
        modeWriteToUser = "размер 900:506"
        modeToChagne = "crop"
    else:
        modeWriteToUser = "оригинальный размер"
        modeToChagne = "original"
    mode.change_mode(message.from_user.id, modeToChagne)
    await message.answer(f"Ваш режим изменен на - <b>{modeWriteToUser}</b>\nЧтобы изменить режим обратно повторно введите команду '/mode'", parse_mode="html")

@dp.message_handler(content_types=["photo"])
async def photo(message: types.Message):
    randomFileName = random.randint(9999, 999999)
    await message.photo[-1].download(destination_file=f'photos/{randomFileName}.jpg')
    userMode = mode.check(message.from_user.id)
    if userMode == "original":
        modeWriteToUser = "оригинальный размер"
    else:
        modeWriteToUser = "размер 900:506"
    msg_id = await message.answer(f"Получено фото. Ваш режим - <b>{modeWriteToUser}</b>. Идет обработка, подождите", parse_mode="html")
    dots = 1
    for i in range(7):
        if dots > 3:
            dots = 1
        await bot.edit_message_text(f"Получено фото. Ваш режим - <b>{modeWriteToUser}</b>. Идет обработка, подождите{'.' * dots}", message.from_user.id, msg_id["message_id"], parse_mode="html")
        dots += 1
        time.sleep(0.5)
    croperData = croper(f'{randomFileName}.jpg', userMode)
    file_name = croperData[0]
    imageSize = croperData[1]
    await bot.send_photo(message.from_user.id, open(f'photos/{file_name}', 'rb'), caption=f"Ваше фото готово\nРазмер изображения - {imageSize}", parse_mode="html")
    os.remove(f"photos/{file_name}")
    os.remove(f"photos/{randomFileName}.jpg")

@dp.message_handler(content_types=["text"])
async def photo(message: types.Message):
    randomFileName = random.randint(9999, 999999)
    try:
        p = requests.get(f"{message.text}")
        out = open(f"photos/{randomFileName}.jpg", "wb")
        out.write(p.content)
        out.close()

        userMode = mode.check(message.from_user.id)
        if userMode == "original":
            modeWriteToUser = "оригинальный размер"
        else:
            modeWriteToUser = "размер 900:506"
        msg_id = await message.answer(f"Получена ссылка на фото. Ваш режим - <b>{modeWriteToUser}</b>. Идет обработка, подождите", parse_mode="html")
        dots = 1
        for i in range(7):
            if dots > 3:
                dots = 1
            await bot.edit_message_text(f"Получена ссылка на фото. Ваш режим - <b>{modeWriteToUser}</b>. Идет обработка, подождите{'.' * dots}", message.from_user.id, msg_id["message_id"], parse_mode="html")
            dots += 1
            time.sleep(0.5)
        croperData = croper(f'{randomFileName}.jpg', userMode)
        file_name = croperData[0]
        imageSize = croperData[1]
        await bot.send_photo(message.from_user.id, open(f'photos/{file_name}', 'rb'), caption=f"Ваше фото готово\nРазмер изображения - {imageSize}", parse_mode="html")
        os.remove(f"photos/{file_name}")
        os.remove(f"photos/{randomFileName}.jpg")
    except:
        await message.answer(f"Получена неверная ссылка! Убедитесь в правильности и попробуйте еще раз!", parse_mode="html")
        try:
            os.remove(f"photos/{file_name}")
            os.remove(f"photos/{randomFileName}.jpg")
        except:
            pass