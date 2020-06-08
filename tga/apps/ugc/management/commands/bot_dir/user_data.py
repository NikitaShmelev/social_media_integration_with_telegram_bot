from email_validator import validate_email, EmailNotValidError
from telegram import ReplyKeyboardRemove
# from telegram import Chat
from telegram.error import BadRequest
from random import randint
import smtplib
from .bot_data import BotState
from .post_data import Post
from .translates import translates
from home.models import UserProfile
from .keyboards import LANGUAGE_EN, LANGUAGE_RU, \
    start_keyboard, conifrm_keyboard, post_keyboard, language_keyboard, email_keyboard, \
    regisration_keyboard, channels_keyboard, unpublished_keyboard, find_post_keyboard, \
    help_keyboard, start_page_keyboard

DATABASE_PATH = './db.sqlite3'

class UserObject():


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
        self.current_channel = None
        self.append_channel = False
        self.remove_channel = False
        self.channels = [False, ]
        self.post = None
        self.unpublished_keyboard = False
        self.change_language = False
        
        self.update_post = False
        self.add_location = False
        self.add_media = False
        
        self.event = [False, False]
        self.publish = False
        
        
        self.save_and_publish = False
        self.update_and_publish = False
        self.all_channels = False
        self.show_unpublished_posts = False
        
        self.unpublished_posts = {} # key - created_at (DATETIME)
        
        self.cancel_post = False
        self.current_post_id = None

        

       


    
    
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
        if self.data in ['English', 'Русский'] or self.change_language:
            if self.data not in [translates['English']['CHANGE_LANGUAGE'], translates['Русский']['CHANGE_LANGUAGE']]:
                self.language = self.data
                if not self.email:
                    self.check_email = True
                    update.effective_chat.send_message(
                        text=translates[self.language]['language_selected'],
                    )
                    update.effective_chat.send_message(
                        text=translates[self.language]['tap_email'],
                        reply_markup=ReplyKeyboardRemove(),
                        )
                if self.change_language:
                    UserProfile.objects.filter(user_id=self.chat_id).update(language=self.language)
                    update.effective_chat.send_message(
                        text=translates[self.language]['language_selected'],
                        reply_markup=start_keyboard(self)
                    )
                self.select_language = False
                self.change_language = False
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
    

    def add_channel(self, update, context):
        if self.data != translates[self.language]['add_channel'] and self.append_channel:
            if 'https://t.me/' in self.data:
                self.current_channel = f'@{self.data[13:]}'
            elif '@' in self.data:
                self.current_channel = self.data
            else:
                self.current_channel = f'@{self.data}'
            if self.current_channel not in self.channels:
                try:
                    context.bot.send_message(                        
                        chat_id=self.current_channel,
                        text=translates[self.language]['bot_added'],
                    )
                    conn, cur =  BotState().open_db_connection()
                    cur.execute(
                        'INSERT INTO home_channel (channel_id, USER_ID) VALUES(?,?)',
                        (self.current_channel, self.chat_id)
                        )
                    conn.commit()
                    BotState().close_db_connection(conn, cur)
                    update.effective_chat.send_message(
                        text=translates[self.language]['channel_added'],
                        reply_markup=start_keyboard(self),
                    )
                    self.channels.append(self.current_channel)
                    self.clear_variables()
                    del conn, cur
                except:
                    update.effective_chat.send_message(
                        text=translates[self.language]['cant_add_bot'],
                        reply_markup=start_page_keyboard(self),    
                    )
            else:
                update.effective_chat.send_message(
                    text='This channel in already exists. Send another channel.',
                    reply_markup=start_page_keyboard(self),
                )
        else:
            update.effective_chat.send_message(
                text='Send channel id\n(You can send without @) or send channel link',
                reply_markup=start_page_keyboard(self),
                )

    def delete_channel(self, update):
        if self.remove_channel:
            if self.data not in [translates[self.language]['CONFIRM_NO'], translates[self.language]['CONFIRM_YES']]:
                if 'https://t.me/' in self.data:
                    self.current_channel = f'@{self.data[13:]}'
                elif '@' in self.data:
                    self.current_channel = self.data
                else:
                    self.current_channel = f'@{self.data}'
            else:
                if self.data == translates[self.language]['CONFIRM_YES']:
                    conn, cur =  BotState().open_db_connection()
                    cur.execute(
                        "DELETE FROM home_channel WHERE channel_id=? and user_id=?",
                        (self.current_channel, self.chat_id)
                        )
                    conn.commit()
                    BotState().close_db_connection(conn, cur)
                    self.clear_variables()
                    update.effective_chat.send_message(
                        text='channel_removed',
                        reply_markup=start_keyboard(self),

                    )
                    del conn, cur
                    return True
                else:
                    self.clear_variables()
                    update.effective_chat.send_message(
                        text='Post removing was successfully canceled.',
                        reply_markup=start_keyboard(self),
                    )
                    return False
            if self.current_channel in self.channels and self.data != translates[self.language]['remove_channel']:
                update.effective_chat.send_message(
                    text='confirm_action',
                    reply_markup=conifrm_keyboard(self),
                )
                
            else:
                if len(self.channels) > 1:
                    update.effective_chat.send_message(
                        text='Send correct channel id(You can send without @) or send channel link.\n'
                            'Also you can select ypur channel fron channels list',
                        reply_markup=channels_keyboard(self)
                    )
                else:
                    self.clear_variables()
                    update.effective_chat.send_message(
                        text='You have no channels to remove',
                        reply_markup=start_keyboard(self)
                    )
        else:
            update.effective_chat.send_message(
					text=translates[self.language]['list_of_channels'],
					reply_markup=channels_keyboard(self),
				)
            
            
    def create_post_button(self, update):
        if self.event[0]:
            update.effective_chat.send_message(
                    text=translates[self.language]['already'],
					reply_markup=post_keyboard(self),
				)
            # add show post
        else:
            try:
                self.post.clear_post()
                self.event = [False, False]
            except:
                self.post = Post('some_id', 'some_date')
                # self.event[0] = True
            self.event[0] = True
            update.effective_chat.send_message(
                text=translates[self.language]['Post_creation'],
                reply_markup=post_keyboard(self),
            )

        
        
    def clear_variables(self):
        self.current_channel = None
        self.append_channel = False
        self.remove_channel = False
        self.language_change = False
        self.cancel_post = False
        self.save_and_publish = False
        self.update_and_publish = False
        self.all_channels = False
        self.show_unpublished_posts = False
        self.unpublished_keyboard = False
        self.publish = False
        # self.update_post = False
        self.add_media = False
        if self.post:
            self.post.text[0] = False
            self.post.add_location = False
            self.post.add_media = False
            
            