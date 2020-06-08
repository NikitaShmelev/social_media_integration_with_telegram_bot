import os
import sys 
import sqlite3
from logging import getLogger
from datetime import datetime

from home.models import UserProfile, Channel, Post, PostMedia, PostLocation 

from .post_data import Post
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


    def open_db_connection(self):
        conn = sqlite3.connect(self.DATABASE_PATH)
        cur = conn.cursor()
        return conn, cur


    def close_db_connection(self, conn, cur):
        cur.close()
        conn.close()
        del conn, cur


    def take_users(self):
        conn, cur = self.open_db_connection()
        cur.execute("SELECT USER_ID from home_userprofile")
        self.users_ids = tuple(i[0] for i in cur.fetchall())
        self.close_db_connection(conn, cur)
        del conn, cur


    def take_emails(self):
        conn, cur = self.open_db_connection()
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
        """This method takes all user's data from database

        Arguments:
            new_user_object -- [
                This object must have chat_id atribute.
                This function will be called at sign in stage of user.
                ]

        Returns:
            user_object -- [user with all data from database]
        """
        conn, cur = self.open_db_connection()
        user.user_registration = True
        cur.execute("SELECT * from home_userprofile WHERE user_id=?",(user.chat_id, ))
        data = cur.fetchall()[0]
        user.username, user.language, user.email = data[2], data[3], data[4]
        cur.execute("SELECT channel_id from home_channel WHERE user_id=?",(user.chat_id, ))
        user.channels += [i[0] for i in cur.fetchall()]
        cur.execute("SELECT * from home_post WHERE user_id=? and PUBLISHED=?",(user.chat_id, 0))
        user.unpublished_posts = self.get_posts(user.chat_id)    
        print(
            '\n\nUser loged in\n'
            f'Username: {user.username}\nID: {user.chat_id}\nEmail: {user.email}\n\n\n'
            )
        self.close_db_connection(conn, cur)
        del conn, cur, data
        return user


    def get_posts(self, chat_id):
        conn, cur = self.open_db_connection()
        cur.execute("SELECT * from home_post WHERE user_id=? and PUBLISHED=?",(chat_id, 0))
        posts = cur.fetchall()
        unpublished_posts = {}
        for post in posts:
            unpublished_posts[str(post[1])] = Post(
                post_id=post[0],
                created_at=post[1],
                text=[False, post[2]],
            )
            if post[4]:
                '''MEDIA'''
                cur.execute("SELECT * from home_postmedia WHERE post_id=?",(post[0],))
                try:
                    media_data = cur.fetchall()[0]
                    unpublished_posts[post[1]].media = {
                        0: True,
                        1: media_data[1],
                        2: media_data[2],
                        3: media_data[3],
                        4: media_data[4],
                        5: media_data[5],
                        6: media_data[6],
                        7: media_data[7],
                        8: media_data[8],
                        9: media_data[9],
                        10: media_data[10],
                    }
                    del media_data
                except IndexError:
                    unpublished_posts[post[1]].media = {
                        0: True,
                        1: '',
                        2: '',
                        3: '',
                        4: '',
                        5: '',
                        6: '',
                        7: '',
                        8: '',
                        9: '',
                        10: '',
                    }
            if post[5]:
                '''location'''
                cur.execute("SELECT * from home_postlocation WHERE post_id=?",(post[0],))
                try:
                    location_data = cur.fetchall()[0]
                    unpublished_posts[post[1]].location = [True, location_data[1], location_data[2]]
                    del location_data
                except IndexError:
                    unpublished_posts[post[1]].location = [False, '', '']
        self.close_db_connection(conn, cur)
        return unpublished_posts