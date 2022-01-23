from json import loads
from telegram import Update
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from telegram.ext import Updater, CallbackContext, Filters

from telegram.utils.helpers import create_deep_linked_url

from friendly_handler import FriendlyHandler
# from db_handler import *
from db_manager import helpers

from decouple import config
from uuid import uuid4

API_TOKEN = config('API')
Bot = Updater(API_TOKEN)
dis = FriendlyHandler(Bot)

lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

bot_image = "https://ibb.co/dbvBx9k"
_404_iamge = ""


@dis.command_handler('start')
def start(update: Update, context: CallbackContext):

    if update.effective_chat.type != "private":
        text = "جهت استفاده از ربات، وارد ربات شوید\n\n" \
            "🆔: t.me/HLD202bot?start"
        update.message.reply_photo(bot_image, caption=text)
        return 0


    keyboards = [
        [KeyboardButton('سینمایی 🎬'),
         KeyboardButton('سریالی 🎥'), ],

        [KeyboardButton('OVAs'),
         KeyboardButton('Specials'), ],

        [KeyboardButton('جستجو 🔍'),
         KeyboardButton('درخواست 📬'), ],

        [KeyboardButton('حمایت مالی 🆘'), ],
        [KeyboardButton('بستن ربات ✖️'), ],
    ]

    description = "✨ به انیمه لند خوش آمدید ✨" \
                  "\n\n📌 از طریق ربات انیمه لند می توانید انیمه های دوبله شده را به زبان های انگلیسی، ژاپنی و آلمانی دانلود کنید " \
                  "\n\nلطفا نوع انیمه ی خود را انتخواب کنید:"

    markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True, one_time_keyboard=True)
    update.effective_message.reply_photo(photo=bot_image, caption=description, reply_markup=markup)



@dis.message_handler(None)#filters=Filters.regex("^(Specials|OVAs|سینمایی 🎬|سریالی 🎥|جستجو 🔍|درخواست 📬|حمایت مالی 🆘|بستن ربات ✖️)$"))
def messages(update: Update, context: CallbackContext):
    text = update.effective_message.text
    if text == "Specials": specials(update, context)
    if text == "OVAs": ovas(update, context)
    if text == "سریالی 🎥": series(update, context)
    if text == "سینمایی 🎬": movies(update, context)
    if text == 'بستن ربات ✖️': 
        update.message.reply_text(
        'ربات بسته شد\n'\
        'برای شروع دوباره از /start استفاده کنید'
        , reply_markup=ReplyKeyboardRemove())


def movies(update: Update, context):
    message_id = update.effective_message.message_id
    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('⏰ جدید ترین انیمه های سینمایی ⏰', switch_inline_query_current_chat='جدید ترین انیمه های سینمایی')],
            [InlineKeyboardButton('📈 برترین انیمه های سینمایی 📈', switch_inline_query_current_chat='برترین انیمه های سینمایی')],

            [
                InlineKeyboardButton('🗂 دسته ها 🗂', callback_data='themes'),
                InlineKeyboardButton('📂 ژانر ها 📂', callback_data='genres')
             ],
            [
                InlineKeyboardButton('جست و جو', switch_inline_query_current_chat=''),
                InlineKeyboardButton('جست و جوی پیشرفته', callback_data='advancedSearch')
             ],

            [InlineKeyboardButton('🆘 حمایت مالی 🆘', callback_data='donation')]
        ],
    )
    update.message.reply_photo(
        photo=bot_image, 
        caption="🎬 لطفا دسته ی خود را انتخواب کنید", 
        reply_to_message_id=message_id,
        reply_markup=markup)


def series(update, context):
    message_id = update.effective_message.message_id
    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('⏰ جدید ترین انیمه های سریالی ⏰', switch_inline_query_current_chat='جدید ترین انیمه های سریالی')],
            [InlineKeyboardButton('📈 برترین انیمه های سریالی 📈', switch_inline_query_current_chat='برترین انیمه های سریالی')],

            [
                InlineKeyboardButton('🗂 دسته ها 🗂', callback_data='themes'),
                InlineKeyboardButton('📂 ژانر ها 📂', callback_data='genres')
             ],
            [
                InlineKeyboardButton('جست و جو', switch_inline_query_current_chat=''),
                InlineKeyboardButton('جست و جوی پیشرفته', callback_data='advancedSearch')
             ],

            [InlineKeyboardButton('🆘 حمایت مالی 🆘', callback_data='donation')]
        ],
    )
    update.message.reply_photo(
        photo=bot_image, 
        caption="🎥 لطفا دسته ی خود را انتخواب کنید", 
        reply_to_message_id=message_id,
        reply_markup=markup)


def ovas(update: Update, context):
    message_id = update.effective_message.message_id

    update.message.reply_photo(
        photo=bot_image, 
        caption="متاسفانه این بخش هنوز فعال نشده...", 
        reply_to_message_id=message_id)


def specials(update: Update, context):
    message_id = update.effective_message.message_id

    update.message.reply_photo(
        photo=bot_image, 
        caption="متاسفانه این بخش هنوز فعال نشده...", 
        reply_to_message_id=message_id)


@dis.callback_query_handler()
def callback_query(update: Update, context: CallbackContext):
    pass


@dis.inline_query_handler()
def inline_query(update: Update, context: CallbackContext):
    query = update.inline_query.query
    bot = context.bot

    if query == "جدید ترین انیمه های سریالی":
        results = []
        with open('db/anime_type.json', 'r') as f: series = loads(f.read())['series']
        for anime_code in series:
            img, tit, des = helpers.load_preview('db/anime_list.json', anime_code) 
            results.append(InlineQueryResultArticle(
                uuid4(), 
                thumb_url=img, 
                title=tit, 
                input_message_content=InputTextMessageContent(
                    create_deep_linked_url(bot.username, f"sr{anime_code}")
                ), 
                description=des))
        
        update.inline_query.answer(results, 10)

    if query == "جدید ترین انیمه های سینمایی":
        results = []
        with open('db/anime_type.json', 'r') as f: movies = loads(f.read())['movies']
        for anime_code in series:
            img, tit, des = helpers.load_preview('db/anime_list.json', anime_code) 
            results.append(InlineQueryResultArticle(
                uuid4(), 
                thumb_url=img, 
                title=tit, 
                input_message_content=InputTextMessageContent(
                    create_deep_linked_url(bot.username, f"sr{anime_code}")
                ), 
                description=des))
        
        update.inline_query.answer(results, 10)


if __name__ == '__main__':
    print("[BOT'S WORKING]")
    Bot.start_polling()
    Bot.idle()
