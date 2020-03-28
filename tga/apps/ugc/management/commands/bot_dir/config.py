from logging import getLogger
import os, sys


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


class Settings():
    def __init__(self):
        self.token = '902495020:AAH42KO9_MpcBLa0XHRjB4wg1yOesgsEf7Y'
        self.users = []
        self.users_emails = []
        self.path = os.getcwd()[0:-32]
        self.request_count = 0


class User_params():    
     def __init__(self):
        self.chat_id = None
        self.data = ''
        self.email = None
        self.date = None
        self.add_channel = False
        self.remove_channel = False
        self.media_id = ['', ''] # First - photo, second - movie
        self.check_list = []
        self.event = [False, False]
        self.text = [False, '']
        self.location = [False, '', '']
        self.current_channel = ''
        self.publish = False
        self.save_post = False
        self.update_post = False
        self.unpublished_keyboard = False
        self.show_unpublished_posts = False
        self.media = {
            0: False,
            1: '',
            2: '',
            3: '',
            4: '',
            5: '',
            6: '',
            7: '',
            8: '',
            9: '',
        }
        self.channels = []
        self.unpublished_posts = {}
        self.unpublished_posts_reverse = {} # switch key with value
        self.current_post_id = None
        self.all_channels = False
        self.code = [None, False]
        self.emails = []
        self.access = False
        self.user_registration = False
        self.username = False
        self.get_name = False
        self.language = ''
        self.language_change = False
        self.check_email = False
        self.help = False


class User():
    def __init__(self):
        self.user = {}      
