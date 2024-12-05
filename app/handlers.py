import aiosmtplib, logging
from aiogram import types, F, Bot
from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from email.message import EmailMessage

from config import token

bot = Bot(token=token)

from app.keyrboards import *
from config import SMTP_PASSWORD, SMTP_USER

router = Router()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = SMTP_USER
SMTP_PASSWORD = SMTP_PASSWORD

async def send_email(to_email, send_body):
    message = EmailMessage()
    message.set_content(send_body)
    message['Subject'] = 'Сообщение от бота'
    message['From'] = SMTP_USER
    message['To'] = to_email

    try:
        logging.info(f'Отправка email на {to_email}')
        await aiosmtplib.send(
            message,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD
        )
        logging.info("Успешно отправлена")
    except Exception as e:
        logging.info("Ошибка", e)


class sending_email(StatesGroup):
    user_email = State()

@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    await message.answer("Привет\nВведите почту которому вы хотите отправить сообщение!")
    await state.set_state(sending_email.user_email)

@router.message(sending_email.user_email)
async def send_to_email(message: types.Message, state: FSMContext):
    while True:
        if '@gmail.com' in message.text:
            await state.update_data(user_email=message.text)
            data = await state.get_data()
            global user_email
            user_email = data['user_email']
            await state.clear()
            await message.answer(f"Вы выбрали адрес {user_email}\nЧто вы хотите отправить", reply_markup=inline_button)
            break

        else:
            await message.answer('Пожалуйста введите правильный адрес почты')
            break

@router.callback_query(F.data == 'back')
async def back(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите почту которому вы хотите отправить сообщение!")
    await state.set_state(sending_email.user_email)

@router.message(sending_email.user_email)
async def back_1(message: types.Message, state: FSMContext):
    while True:
        if '@gmail.com' in message.text:
            await state.update_data(user_email=message.text)
            data = await state.get_data()
            global user_email
            user_email = data['user_email']
            await state.clear()
            await message.answer(f"Вы выбрали адрес {user_email}\nЧто вы хотите отправить", reply_markup=inline_button)
            break

        else:
            await message.answer('Пожалуйста введите правильный адрес почты')
            break

class sending_message(StatesGroup):
    send_message = State()

@router.callback_query(F.data == 'message')
async def message_send(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите сообщение")
    await state.set_state(sending_message.send_message)

@router.message(sending_message.send_message)
async def message_send_1(message: types.Message, state: FSMContext):
    await state.update_data(send_message=f'Пользователь телеграм бота {message.from_user.full_name} отправил вам сообщение:\n{message.text}')
    data = await state.get_data()
    send_message = data['send_message']
    await send_email(user_email, send_message)
    await state.clear()
    await message.answer(f"Сообщение отправлено на адрес {user_email}", reply_markup=inline_button)

class sending_photo(StatesGroup):
    send_photo = State()

@router.callback_query(F.data == 'photo')
async def photo_send(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправте фото через ссылку")
    await state.set_state(sending_photo.send_photo)

@router.message(sending_photo.send_photo)
async def photo_send_1(message: types.Message, state: FSMContext):
    while True:
        if 'https:' in message.text:
            await state.update_data(send_photo=f'Пользователь телеграм бота {message.from_user.full_name} отправил вам фотографию:\n{message.text}')
            data = await state.get_data()
            send_photo = data['send_photo']
            await send_email(user_email, send_photo)
            await message.answer(f"Ссылка фотографии отправлено на адрес {user_email}", reply_markup=inline_button)
            break

        else:
            await message.answer('Пожалуйста введите правильную ссылку')
            break
    
class sending_video(StatesGroup):
    send_video = State()

@router.callback_query(F.data == 'video')
async def video_send(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправте видео через ссылку")
    await state.set_state(sending_video.send_video)

@router.message(sending_video.send_video)
async def video_send_1(message: types.Message, state: FSMContext):
    while True:
        if 'https:' in message.text:
            await state.update_data(send_video=f'Пользователь телеграм бота {message.from_user.full_name} отправил вам видео:\n{message.text}')
            data = await state.get_data()
            send_video = data['send_video']
            await send_email(user_email, send_video)
            await message.answer(f"Видео ссылка отправлено на адрес {user_email}", reply_markup=inline_button)
            break

        else:
            await message.answer('Пожалуйста введите правильную ссылку')
            break

class sending_audio_files(StatesGroup):
    send_audio_files = State()

@router.callback_query(F.data == 'audio_files')
async def audio_send(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправте аудио")
    await state.set_state(sending_audio_files.send_audio_files)

@router.message(sending_audio_files.send_audio_files)
async def audio_send_1(message: types.Message, state: FSMContext):
    await state.update_data(send_audio_files=f'Пользователь телеграм бота {message.from_user.full_name} отправил вам аудио:\n{message.audio.file_id}')
    data = await state.get_data()
    send_audio_files = data['send_audio_files']
    await send_email(user_email, send_audio_files)
    await message.answer(f"Аудио ссылка отправлено на адрес {user_email}", reply_markup=inline_button)