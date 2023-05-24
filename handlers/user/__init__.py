from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from .help import bot_help
from .start import bot_start, receive_audio, chat


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(receive_audio, content_types=[types.ContentType.VOICE])
    dp.register_message_handler(bot_help, CommandHelp())
    dp.register_message_handler(chat, content_types=[types.ContentType.TEXT])
