
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.request import Request

from django.core.management.base import BaseCommand
from django.conf import settings

from ugc.models import Message
from ugc.models import Profile

from logging import getLogger
from random import randint

from .bot_dir.utils import debug_requests
from .bot_dir.config import Settings, User, User_params, load_config
from .bot_dir.translates import translates
from .bot_dir.functions import take_users, take_user_data, cancel_post,\
    add_user_to_database, location_for_post, media_for_post, \
    text_for_post, show_created_post, save_post, \
    create_post_button, change_language, take_emails, \
    send_email, remove_channel, add_channel, \
    find_post, update_post
from .bot_dir.keyboards import LANGUAGE_EN, LANGUAGE_RU, \
    start_keyboard, conifrm_keyboard, post_keyboard, language_keyboard, email_keyboard, \
    regisration_keyboard, channels_keyboard, unpublished_keyboard, find_post_keyboard


config = load_config()
logger = getLogger(__name__)
settings = Settings()
user = User()


@debug_requests
def do_start(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id


@debug_requests
def take_text(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id


@debug_requests
def get_media(bot: Bot, update: Update):
	chat_id = update.message.chat_id


@debug_requests
def get_location(bot: Bot, update: Update):
    chat_id = update.message.chat_id


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        # 1 -- правильное подключение
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.token,
            base_url=getattr(settings, 'PROXY_URL', None),
        )
        print(bot.get_me())

        # 2 -- обработчики
        updater = Updater(
            bot=bot,
            use_context=True,
        )
        start_handler = CommandHandler(
            "start",
            do_start
        )
    # Message handlers
        text_message_handler = MessageHandler(
            Filters.text,
            take_text
        )
        img_message_handler = MessageHandler(
            Filters.photo,
            get_media
        )
        video_message_handler = MessageHandler(
            Filters.video,
            get_media
        )
        location_message_handler = MessageHandler(
            Filters.location,
            get_location
        )
        # dispatchers
        updater.dispatcher.add_handler(start_handler)
        updater.dispatcher.add_handler(text_message_handler)
        updater.dispatcher.add_handler(img_message_handler)
        updater.dispatcher.add_handler(location_message_handler)
        updater.dispatcher.add_handler(video_message_handler)
        updater.start_polling()
        updater.idle()
        # message_handler = MessageHandler(Filters.text, do_echo)
        # updater.dispatcher.add_handler(message_handler)
        # updater.dispatcher.add_handler(CommandHandler('count', do_count))

        # 3 -- запустить бесконечную обработку входящих сообщений
