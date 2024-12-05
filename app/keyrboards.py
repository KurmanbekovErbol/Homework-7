from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сообщения', callback_data='message'), InlineKeyboardButton(text='Фото', callback_data='photo')],
    [InlineKeyboardButton(text='Видео', callback_data='video'), InlineKeyboardButton(text='Аудиофайлы', callback_data='audio_files')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])
