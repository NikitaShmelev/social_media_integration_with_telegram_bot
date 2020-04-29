import os
import sys 
import sqlite3
from logging import getLogger
from home.models import UserProfile #, Channel, Post, PostMedia, PostLocation 
from .user_data import User_Object
try:
	from .keyboards import LANGUAGE_EN, LANGUAGE_RU, \
		start_keyboard, conifrm_keyboard, post_keyboard, language_keyboard, email_keyboard, \
		regisration_keyboard, channels_keyboard, unpublished_keyboard, find_post_keyboard, \
		help_keyboard
except ImportError:
	pass

logger = getLogger(__name__)


def load_config():
    conf_name = os.environ.get("TG_CONF")
    if conf_name is None:
        conf_name = "development"
    try:
        return logger.debug("Loaded config \"{}\" - OK".format(conf_name))
    except (TypeError, ValueError, ImportError):
        logger.error("Invalid config \"{}\"".format(conf_name))
        sys.exit(1)


class BotState():


    def __init__(self):
        self.token = '902495020:AAH42KO9_MpcBLa0XHRjB4wg1yOesgsEf7Y'
        self.users_ids = list()
        self.users = {}
        self.emails = tuple()
        self.request_count = 0
        self.DATABASE_PATH = './db.sqlite3'


    def open_db_connection(self, db_path, user=None):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        return conn, cur


    def close_db_connection(self, conn, cur, user=None):
        cur.close()
        conn.close()
        del conn, cur


    def take_users(self):
        conn, cur = self.open_db_connection(self.DATABASE_PATH)
        cur.execute("SELECT USER_ID from home_userprofile")
        self.users_ids = tuple(i[0] for i in cur.fetchall())
        self.close_db_connection(conn, cur)
        del conn, cur


    def take_emails(self):
        conn, cur = self.open_db_connection(self.DATABASE_PATH)
        cur.execute("SELECT email from home_userprofile")
        self.users_emails = [i[0] for i in cur.fetchall()]
        self.close_db_connection(conn, cur)
        del conn, cur


    def add_user_to_database(self, user):
        user_profile = UserProfile(
            user_id=user.chat_id,
            language=user.language,
            username=user.username,
            email=user.email,

        )
        user_profile.save_base()
  

    def take_user_data(self, user):
        conn, cur = self.open_db_connection(self.DATABASE_PATH)
        user.user_registration = True
        cur.execute("SELECT * from home_userprofile WHERE user_id=?",(user.chat_id, ))
        data = cur.fetchall()[0]
        user.username, user.language, user.email = data[2], data[3], data[4]
        cur.execute("SELECT channel_id from home_channel WHERE user_id=?",(user.chat_id, ))
        user.channels = [i[0] for i in cur.fetchall()]
        cur.execute("SELECT id from home_post WHERE user_id=? and PUBLISHED=?",(user.chat_id, 0))
        ids = cur.fetchall()
        cur.execute("SELECT created_at from home_post WHERE user_id=? and PUBLISHED=?",(user.chat_id, 0))
        posts = cur.fetchall()
        for date in enumerate(posts):
            user.unpublished_posts[ids[date[0]][0]] = date[1][0]
            user.unpublished_posts_reverse[date[1][0]] = ids[date[0]][0]
        print(
            '\n\nUser loged in\n'
            f'Username: {user.username}\nID: {user.chat_id}\nEmail: {user.email}\n\n\n'
            )
        self.close_db_connection(conn, cur)
        del conn, cur, posts, ids, data
        return user

