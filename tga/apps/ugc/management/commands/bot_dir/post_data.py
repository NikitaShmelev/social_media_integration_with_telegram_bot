import sqlite3

from telegram import ReplyKeyboardRemove
# from telegram.error import TimedOut
from telegram import Bot, Update, Location, InputMediaPhoto, InputMediaVideo
from telegram import ParseMode

from datetime import datetime 
from time import sleep

from .keyboards import LANGUAGE_EN, LANGUAGE_RU, \
    start_keyboard, conifrm_keyboard, post_keyboard, language_keyboard, email_keyboard, \
    regisration_keyboard, channels_keyboard, unpublished_keyboard, find_post_keyboard, \
    help_keyboard, start_page_keyboard
from .translates import translates

DATABASE_PATH = './db.sqlite3'


class Post:

    
    def __init__(
            self, post_id=None, created_at=None, 
            text=[False, ''], location=[False, '', ''], 
            media={
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
                10: '',
                }):
        self.post_id = post_id # мб не надо
        self.created_at = created_at
        self.text = text
        self.location = location
        self.media = media
        self.media_id = ['', ''] # First - photo, second - movie
        self.check_list = []
        self.saved = False 
        
        
        # self.save_post = False
        
        
        self.all_channels = False
        
    
    def add_text(self, update, user):
        user.post.text[0] = False
        user.post.text[1] = user.data
        update.effective_chat.send_message(
                text=translates[user.language]['I got text'],
                reply_markup=post_keyboard(user),
                parse_mode=ParseMode.MARKDOWN
                )
    
    
    
    def send_post(self, update, user, context, chat_id):
        if (user.save_and_publish or user.update_and_publish) and not user.all_channels:
            chat_id = user.data
        text = self.text[1]
        if len(text) <= 1024:
            caption_for_media = text
        else:
            caption_for_media = ''
        if user.post.location[1] != '':
            latitude = user.post.location[1]
            longitude = user.post.location[2]
            json_dict = {
                'latitude': latitude,
                'longitude': longitude
                }
            location = Location.de_json(json_dict, context.bot)
            location.latitude == latitude
            location.longitude == longitude
            context.bot.send_location(
                chat_id=chat_id,
                location=location,
                )
        media = []
        for i in range(1, len(user.post.media)):
            test = user.post.media[i]
            if test != '':
                if test[0] == 'p':
                    if len(media) == 0:
                        media.append(InputMediaPhoto(
                            user.post.media[i][1:],
                            caption_for_media)
                            )
                    else:
                        media.append(InputMediaPhoto(
                            user.post.media[i][1:],)
                            )
                elif test[0] == 'v':
                    if len(media) == 0:
                        media.append(InputMediaVideo(
                            user.post.media[i][1:],
                            caption_for_media)
                            )
                    else:
                        media.append(InputMediaVideo(
                            user.post.media[i][1:],)
                            )
        if len(media) >= 2:
            context.bot.send_media_group(
                chat_id=chat_id,
                media=media,
                )
        if len(media) == 1:
            if self.media[1][0] == 'p':
                context.bot.send_photo(
                    chat_id=chat_id,
                    caption=caption_for_media,
                    photo=user.post.media[1][1:],
                    )
            else:
                context.bot.send_video(
                    chat_id=chat_id,
                    caption=caption_for_media,
                    video=user.post.media[1][1:],
                    )
        try:
            if len(media) == 0 and text or caption_for_media == '':
                context.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                )
        except:
            pass
    
    
    def show_post(self, update, user, context):
        """[summary]

        Arguments:
            update {class 'telegram.update.Update'} -- [description]
            user {[type]} -- [description]
            context {class 'telegram.ext.callbackcontext.CallbackContext'} -- [description]
        """
        if user.save_and_publish or user.update_and_publish:
            if not self.saved:
                self.saved = True
                if user.update_and_publish:
                    self.publish = True
                    self.update_post(user)
                else:
                    self.save(user)
            if user.all_channels:
                for channel in user.channels[1:]:
                    self.send_post(
                        update, user, context, channel
                    )
                    sleep(1)
            else:
                try:
                    self.send_post(
                        update, user, context, user.data
                    )
                    sleep(1)
                except:
                    # TimedOut
                    sleep(10)
        else:
            self.send_post(
                update, user, context, user.chat_id
                )
    
    
    def clear_post(self):
        """
            Clear all atributes. This is prepair 
            for next post creation
        """
        self.post_id=None
        self.created_at=None
        self.text=[False, '']
        self.location=[False, '', '']
        self.media={
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
            10: '',
            }
        self.media_id = ['', ''] # First - photo, second - movie
        self.check_list = []
        self.publish = False
        self.all_channels = False
        self.saved = False


        
        
        
    def save(self, user):
        print(self.location, 'SAVE_MONENT')
        if self.location[1] != '':
            location = True
        else:
            location = False
        if self.media[1] != '':
            media = True
        else:
            media = False
        if user.save_and_publish:
            publish = True
        else:
            publish = False
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()
        post_date = datetime.today().strftime('"%A, %d. %B %Y %H:%M:%S"')
        
        cur.execute('INSERT INTO home_post ('
                    'USER_ID,CREATED_AT,POST_TEXT,LOCATION,MEDIA,CREATOR_NAME,PUBLISHED) '
                    'VALUES(?,?,?,?,?,?,?)',
         (
            user.chat_id, post_date, self.text[1],
            location, media, user.username, publish
            )
        )
        conn.commit()
        cur.execute('SELECT id FROM home_post WHERE user_id=?',(user.chat_id, ))
        user.current_post_id = cur.fetchall()[-1][0]
        if media:
            cur.execute('INSERT INTO home_postmedia (POST_ID,MEDIA_1,MEDIA_2,MEDIA_3,MEDIA_4,MEDIA_5,MEDIA_6,MEDIA_7,MEDIA_8,MEDIA_9, MEDIA_10)'
                ' VALUES(?,?,?,?,?,?,?,?,?,?,?)',(
                    user.current_post_id, self.media[1], self.media[2], self.media[3], self.media[4],
                    self.media[5], self.media[6], self.media[7], self.media[8], self.media[9],self.media[10],
                    )
            )
            conn.commit()
        if location:

            cur.execute('INSERT INTO home_postlocation (POST_ID,LATITUDE,LONGITUDE)'
                ' VALUES(?,?,?)',
            (
                user.current_post_id, self.location[1], self.location[2],
            )
            )
            conn.commit()
        cur.close()
        conn.close()
        if not user.save_and_publish:
            user.unpublished_posts[user.current_post_id] = self
        if not self.saved:
            self.clear_post()
            user.event = [False, False]
        return user

    
    def update_post(self, user):
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()
        cur.execute('UPDATE home_post set POST_TEXT=?, LOCATION=?, MEDIA=?,PUBLISHED=? WHERE ID= ?',(user.post.text[1], True, True, user.publish, user.current_post_id))
        conn.commit()
        if cur.execute("SELECT * from home_postmedia WHERE post_id=?", (user.current_post_id, )).fetchall():
            cur.execute('UPDATE  home_postmedia set MEDIA_1=?,MEDIA_2=?,MEDIA_3=?,MEDIA_4=?,MEDIA_5=?,MEDIA_6=?,MEDIA_7=?,MEDIA_8=?,MEDIA_9=?,MEDIA_10=?'
                        ' where post_id=?', (
                            user.post.media[1], user.post.media[2], user.post.media[3], user.post.media[4],
                            user.post.media[5], user.post.media[6], user.post.media[7], user.post.media[8], 
                            user.post.media[9], user.post.media[10], user.current_post_id
                        )
                        )
        conn.commit()
        if cur.execute("SELECT * from home_postlocation WHERE post_id=?",(user.current_post_id, )).fetchall():
            cur.execute('UPDATE  home_postlocation set LATITUDE=?,LONGITUDE=?'
                        ' where post_id=?', (user.post.location[1], user.post.location[2], user.current_post_id))
        conn.commit()
        cur.close()
        conn.close()
        return user