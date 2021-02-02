from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callback_data import buttons_callback

EVT_PICK_QUALITY = 'evt_pick_quality'
EVT_CANCEL = 'evt_cancel'

def create_quality_keyboard(high_itag:int, low_itag:int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard= [
            [
                InlineKeyboardButton(text='Quality max', callback_data=buttons_callback.new(itag=high_itag,evt=EVT_PICK_QUALITY)),
                InlineKeyboardButton(text='Quality min', callback_data=buttons_callback.new(itag=low_itag,evt=EVT_PICK_QUALITY))
            ],
            [
                InlineKeyboardButton(text='Cancel', callback_data=buttons_callback.new(itag=-1,evt=EVT_CANCEL))
            ]
        ]
    )

    