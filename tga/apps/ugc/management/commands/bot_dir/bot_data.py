import os
import sys 
import sqlite3
from logging import getLogger

from home.models import UserProfile #, Channel, Post, PostMedia, PostLocation 

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
        self.users = list()
        self.emails = tuple()
        self.path = os.getcwd()[0:-32]
        self.request_count = 0
        self.DATABASE_PATH = './db.sqlite3'


    def open_db_connection(self, db_path, user=None):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        return conn, cur


    def close_db_connection(self, conn, cur, user=None):
        cur.close()
        conn.close()


    def take_users(self):
        conn, cur = self.open_db_connection(self.DATABASE_PATH)
        cur.execute("SELECT USER_ID from home_userprofile")
        self.users = tuple(i[0] for i in cur.fetchall())
        self.close_db_connection(conn, cur)


    def take_emails(self):
        conn, cur = self.open_db_connection(self.DATABASE_PATH)
        cur.execute("SELECT email from home_userprofile")
        self.users_emails = [i[0] for i in cur.fetchall()]
        self.close_db_connection(conn, cur)



  


