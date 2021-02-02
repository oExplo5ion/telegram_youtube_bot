from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import CallbackQuery
from pytube import Stream
from botstate import BotState
from pytube import YouTube
from aiogram.utils.callback_data import CallbackData
import logging
import inline_keyboard_markupHelper as InlineKeyboardMarkupHelper
from callback_data import buttons_callback
import youtube_helper

# fields 
API_TOKEN = ''
state = BotState.IDLE
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
quality_callback = CallbackData('quality','url')
youtube = None

# commands
START   = '/start'
HELP    = '/help'

# Keyboard buttons data
QUALITY_HIGH = 'quality_hight'
QUALITY_LOW = 'quality_low'

# handlers
@dp.message_handler(commands=['start'])
async def command_handler(message: types.Message):
    if message.text == START:
        await _send_start(message)

@dp.message_handler(content_types= types.ContentType.TEXT)
async def text_handler(message: types.Message):
    if state == BotState.WAITING_FOR_LINK:
        await _parse_link(message)

@dp.callback_query_handler(buttons_callback.filter(evt=InlineKeyboardMarkupHelper.EVT_PICK_QUALITY))
async def _download_video(call: CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup(reply_markup=None)

    global youtube
    if youtube is None:
        return
    
    itag = callback_data.get('itag')
    file = youtube_helper.download(youtube=youtube, itag=itag, path='videos')

    # TODO: upload a file to user and delete it from disk afterwards


@dp.callback_query_handler(buttons_callback.filter(evt=InlineKeyboardMarkupHelper.EVT_CANCEL))
async def _hide_keyboard(call: CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup(reply_markup=None)

# handler reaction funcs
async def _send_start(message: types.Message):
    global state
    state = BotState.WAITING_FOR_LINK
    await message.answer(text='кидай ссылку видео в YouTube')

# funcs
async def _parse_link(message: types.Message):
    global youtube
    youtube = YouTube(message.text)
    streams = youtube.streams

    itag_high = streams.get_highest_resolution().itag
    itag_low = streams.get_lowest_resolution().itag

    keyboard = InlineKeyboardMarkupHelper.create_quality_keyboard(high_itag=itag_high, low_itag=itag_low)

    global state
    state = BotState.WAITING_FOR_RESOLUTION
    await message.answer(text=youtube.title, reply_markup=keyboard)