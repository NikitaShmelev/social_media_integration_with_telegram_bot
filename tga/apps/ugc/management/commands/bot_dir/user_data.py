from email_validator import validate_email, EmailNotValidError
from telegram import ReplyKeyboardRemove
from random import randint
import smtplib

from .translates import translates
try:
	from .keyboards import LANGUAGE_EN, LANGUAGE_RU, \
		start_keyboard, conifrm_keyboard, post_keyboard, language_keyboard, email_keyboard, \
		regisration_keyboard, channels_keyboard, unpublished_keyboard, find_post_keyboard, \
		help_keyboard
except ImportError:
	pass


class User_Object():


    def __init__(self, chat_id):
        """User's params"""
        self.chat_id = chat_id
        self.data = ''
        self.select_language = False
        self.language = False
        self.email = None
        self.check_email = False
        self.access = False
        self.code = [None, False]
        self.user_registration = False
        self.username = False
        self.get_name = False
        self.language_change = False
        self.help = False
        self.current_channel = None
        self.channels = []
        self.unpublished_posts = {}
        self.unpublished_posts_reverse = {} # switch key with value
        self.current_post_id = None


        self.add_channel = False
        self.remove_channel = False


        self.date = None
        
        self.media_id = ['', ''] # First - photo, second - movie
        self.check_list = []
        self.event = [False, False]
        self.text = [False, '']
        self.location = [False, '', '']
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
        
        self.all_channels = False


    
    
    def validate_user_email(self, update, emails):
        if self.email not in emails:
            try:
                validation = validate_email(self.email)
                update.effective_chat.send_message(
                    text=translates[self.language]['check_email'],
                    reply_markup=email_keyboard(self),
                )
                self.check_email = False
                self.access = True
            except EmailNotValidError:
                update.effective_chat.send_message(
                    text=translates[self.language]['tap_correct_email'],
                    reply_markup=ReplyKeyboardRemove(),
                )
            finally:
                del update
        else:
            update.effective_chat.send_message(
                    text=translates[self.language]['exists_email'],
                    reply_markup=ReplyKeyboardRemove(),
                )

    
    def pick_language(self, update):
        if self.data in ['English', 'Русский']:
            self.select_language = False
            self.check_email = True
            self.language = self.data
            update.effective_chat.send_message(
                text=translates[self.language]['language_selected'],
                )
            update.effective_chat.send_message(
                text=translates[self.language]['tap_email'],
                reply_markup=ReplyKeyboardRemove(),
                )
            
        else:
            update.effective_chat.send_message(
                text=(
                    f"{translates['English']['select_correct_language']} / "
                    f"{translates['Русский']['select_correct_language']}."),
                reply_markup=language_keyboard(self)
                )
        del update
    

    def create_code(self):
        self.access = False
        self.code[1] = True 
        self.code[0] = randint(100000,1000000)
        print(self.code[0])


    def connect_to_email_server(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('apibotpython@gmail.com@', 'botapipassword')
        return server

    
    def send_email_with_code(self, update):
        server = self.connect_to_email_server()
        subject = 'Activation code'
        msg = f'Hello, this is your code {self.code[0]}'
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(self.email, self.email, message)
        server.quit()
        del server
        update.effective_chat.send_message(
                text=translates[self.language]['check_email_for_code'],
                reply_markup=ReplyKeyboardRemove(),
                )


    def check_written_code(self, update):
        try:
            if int(self.data.strip()) == self.code[0]:
                self.get_name = True
                self.code[1] = False
                update.effective_chat.send_message(
                    text=translates[self.language]['name_to_sign_up'],
                )
            else:
                update.effective_chat.send_message(
                    text=translates[self.language]['wrong_code'],
                )
        except ValueError:
            update.effective_chat.send_message(
                text=translates[self.language]['wrong_code'],
                )
    

    