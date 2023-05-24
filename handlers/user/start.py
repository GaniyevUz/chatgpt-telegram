import os

import requests
from aiogram import types
import speech_recognition as sr
from pydub import AudioSegment

from data.config import BOT_TOKEN
import bot
from models.orm import ChatHistory, User
from utils.chatgpt import ask_chatgpt


async def bot_start(msg: types.Message):
    await User.create(msg.from_user.full_name, msg.from_user.username, msg.from_user.idmsg.from_user.id)
    await msg.answer(f'Привет, {msg.from_user.full_name}!')


async def receive_audio(msg: types.Message):
    r = sr.Recognizer()
    voice = await msg.voice.download()
    file = requests.get("https://api.telegram.org/file/bot{0}/{1}".format(
        BOT_TOKEN, voice.name))
    with open('voice_message.ogg', 'wb') as f:
        f.write(file.content)
    # Use pydub to read in the audio file and convert it to WAV format
    sound = AudioSegment.from_file("voice_message.ogg", format="ogg")
    sound.export("voice_message.wav", format="wav")
    os.remove('voice_message.ogg')

    # Use SpeechRecognition to transcribe the voice message
    with sr.AudioFile("voice_message.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    old_messages = await ChatHistory.get_old_messages('friend', 6, msg.from_user.id)

    gpt = ask_chatgpt(text, 'friend', old_messages)
    await ChatHistory.create(text, gpt, 'friend', msg.from_user.id)
    await msg.answer(gpt)


async def chat(msg: types.Message):
    text = msg.text
    role = 'girlfriend'
    old_messages = await ChatHistory.get_old_messages(role, 6, msg.from_user.id)

    gpt = ask_chatgpt(text, role, old_messages)
    await ChatHistory.create(text, gpt, role, msg.from_user.id)
    await msg.answer(gpt)
