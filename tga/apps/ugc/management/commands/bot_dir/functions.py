import sqlite3
from datetime import datetime
from .bot_data import BotState, Users
from telegram import Bot, Update, Location, InputMediaPhoto, InputMediaVideo
from telegram.ext import CallbackContext
from .keyboards import post_keyboard
from .translates import translates
from time import sleep
from home.models import UserProfile #, Channel, Post, PostMedia, PostLocation 


bot_state = BotState()
users = Users()
DATABASE_PATH = './db.sqlite3'


# def create_post_button(user, chat_id, bot: Bot, update: Update):
#     if user.event[0]:
#         # bot.send_message(
#         #     chat_id=chat_id,
#         #     text=translates[user.language]['already'],
#         # )
#         user = cancel_post(user)
    
#     user.event[0] = True
#     bot.send_message(
#         chat_id=update.message.chat_id,
#         text=translates[user.language]['Post_creation'],
#         reply_markup=post_keyboard(user),
#     )
#     return user


# def take_users():
#     conn = sqlite3.connect(DATABASE_PATH)
#     cur = conn.cursor()
#     cur.execute("SELECT USER_ID from home_userprofile")
#     users = [i[0] for i in cur.fetchall()]
#     cur.close()
#     conn.close()
#     return users


# def take_emails():
#     conn = sqlite3.connect(DATABASE_PATH)
#     cur = conn.cursor()
#     cur.execute("SELECT email from home_userprofile")
#     emails = [i[0] for i in cur.fetchall()]
#     cur.close()
#     conn.close()
#     return emails


# def send_email(user):
#     server = smtplib.SMTP('smtp.gmail.com:587')
#     server.ehlo()
#     server.starttls()
#     server.login('apibotpython@gmail.com@', 'botapipassword')
#     subject = 'Activation code'
#     msg = f'Hello, this is your code {user.code[0]}'
#     message = 'Subject: {}\n\n{}'.format(subject, msg)
#     server.sendmail(user.email, user.email, message)
#     server.quit()


# def take_user_data(user, chat_id):
#     user.user_registration = True
#     user.chat_id = chat_id
#     conn = sqlite3.connect(DATABASE_PATH)
#     cur = conn.cursor()
#     cur.execute("SELECT * from home_userprofile WHERE user_id=?",(chat_id, ))
#     data = cur.fetchall()[0]
#     user.username = data[2]
#     user.language = data[3]
#     user.email = data[4]
#     cur.execute("SELECT channel_id from home_channel WHERE user_id=?",(chat_id, ))
#     user.channels = [i[0] for i in cur.fetchall()]
#     cur.execute("SELECT id from home_post WHERE user_id=? and PUBLISHED=?",(chat_id, 0))
#     ids = cur.fetchall()
#     cur.execute("SELECT created_at from home_post WHERE user_id=? and PUBLISHED=?",(chat_id, 0))
#     posts = cur.fetchall()
#     for date in enumerate(posts):
#         user.unpublished_posts[ids[date[0]][0]] = date[1][0]
#         user.unpublished_posts_reverse[date[1][0]] = ids[date[0]][0]
#     cur.close()
#     conn.close()
#     print(
#         '\n\nUser loged in\n'
#         f'Username: {user.username}\nID: {chat_id}\nEmail: {user.email}'
#         )
#     return user


# def change_language(user, chat_id, language):
#     conn = sqlite3.connect(DATABASE_PATH)
#     cur = conn.cursor()
#     cur.execute("UPDATE home_userprofile SET LANGUAGE = ? WHERE USER_ID= ? ", (language ,chat_id))
#     conn.commit()
#     cur.close()
#     conn.close()
#     user.language = language
#     user.change_language = False
#     return user


# def add_channel(user, chat_id):
#     conn = sqlite3.connect(DATABASE_PATH)
#     cur = conn.cursor()
#     cur.execute(
#         'INSERT INTO home_channel (channel_id, USER_ID) VALUES(?,?)',
#         (user.current_channel, chat_id)
#         )
#     conn.commit()
#     cur.close()
#     conn.close()
#     user.channels.append(user.current_channel)
#     return user



# def remove_channel(user, chat_id):
#     conn = sqlite3.connect(DATABASE_PATH)
#     cur = conn.cursor()
#     cur.execute(
#         "DELETE FROM home_channel WHERE channel_id=? and user_id=?",
#         (user.current_channel, chat_id)
#         )
#     conn.commit()
#     cur.close()
#     conn.close()
#     user.channels.remove(user.current_channel)
#     return user



# def add_user_to_database(bot_state, user, chat_id):
#     user.user_registration = True
#     user.get_name = False
#     user.code[1] = False
#     user.check_email = False
#     user.access = False
#     bot_state.users.append(chat_id)
#     bot_user = UserProfile(
#         username=user.username,
#         email=user.email.lower(),
#         language=user.language,
#         user_id=chat_id,
#     )
#     bot_user.save_base()
#     print(
#         '\n\nUser loged in\n'
#         f'Username: {user.username}\nID: {chat_id}\nEmail: {user.email}'
#         )
#     return bot_state, user


# def cancel_post(user):
#     user.event[0] = False
#     user.remove_channel = False
#     user.add_channel = False
#     user.publish = False
#     user.save = False
#     user.show_unpublished_posts = False
#     user.current_channel = ''
#     user.help = False
#     user.media_id = ['', '']  # First - photo, second - movie
#     user.check_list = []
#     user.event = [False, False]
#     user.text = [False, '']
#     user.location = [False, '', '']
#     user.media = {
#         0: False,
#         1: '',
#         2: '',
#         3: '',
#         4: '',
#         5: '',
#         6: '',
#         7: '',
#         8: '',
#         9: '',
#     }
#     user.unpublished_keyboard = False
#     user.current_channel = ''
#     user.current_post_id = None
#     user.date = None
#     return user


# def text_for_post(user):
#     user.text[0] = True #!
#     user.location[0] = False
#     user.media[0] = False
#     return user


# def location_for_post(user):
#     user.text[0] = False
#     user.location[0] = True #!
#     user.media[0] = False
#     return user


# def media_for_post(user):
#     user.location[0] = False
#     user.media[0] = True #!
#     user.text[0] = False
#     return user


# def show_created_post(user, chat_id, bot: Bot, update: Update, context = CallbackContext):


#     def send_post(chat_id):
#         text = user.text[1] + f'\nPost was created by {user.username}'
#         if user.location[1] != '':
#             latitude = user.location[1]
#             longitude = user.location[2]
#             json_dict = {
#                 'latitude': latitude,
#                 'longitude': longitude
#                 }
#             location = Location.de_json(json_dict, bot)
#             location.latitude == latitude
#             location.longitude == longitude
#             bot.send_location(
#                 chat_id=chat_id,
#                 location=location,
#                     )
#         media = []
#         for i in range(1, len(user.media)):
#             test = user.media[i]
#             if test != '':
#                 if test[0] == 'p':
#                     if len(media) == 0:
#                         media.append(InputMediaPhoto(
#                             user.media[i][1:],
#                             text)
#                             )
#                     else:
#                         media.append(InputMediaPhoto(
#                             user.media[i][1:],)
#                             )
#                 elif test[0] == 'v':
#                     if len(media) == 0:
#                         media.append(InputMediaVideo(
#                             user.media[i][1:],
#                             text)
#                             )
#                     else:
#                         media.append(InputMediaVideo(
#                             user.media[i][1:],)
#                             )
#         if len(media) >= 2:
#             bot.send_media_group(
#                 chat_id=chat_id,
#                 media=media,
#                 )
#         if len(media) == 1:
#             if user.media[1][0] == 'p':
#                 bot.send_photo(
#                     chat_id=chat_id,
#                     caption=text,
#                     photo=user.media[1][1:],
#                     )
#             else:
#                 bot.send_video(
#                     chat_id=chat_id,
#                     caption=text,
#                     video=user.media[1][1:],
#                     )
#         if len(media) == 0:
#             bot.send_message(
#                 chat_id=chat_id,
#                 text=text,
#             )
#     if len(user.channels) > 0:
#         if user.all_channels:
#             for i in user.channels:
#                 send_post(i)
#                 sleep(1)
#             user.all_channels = False
#         else:
#             send_post(chat_id)
#     else:
#         send_post(chat_id)
            
#     return user
    

# def save_post(user, chat_id, bot: Bot, update: Update, context = CallbackContext):
#     def save(user):
#         if user.location[1] != '':
#             location = True
#         else:
#             location = False
#         if user.media[1] != '':
#             media = True
#         else:
#             media = False
#         conn = sqlite3.connect(DATABASE_PATH)
#         cur = conn.cursor()
#         post_date = datetime.today().strftime('"%A, %d. %B %Y %H:%M:%S"')
#         cur.execute('INSERT INTO home_post (USER_ID,CREATED_AT,POST_TEXT,LOCATION,MEDIA,CREATOR_NAME,PUBLISHED) VALUES(?,?,?,?,?,?,?)',
#          (
#              chat_id, post_date, user.text[1],
#             location, media, user.username, False
#             )
#         )
#         conn.commit()
#         cur.execute('SELECT id FROM home_post WHERE user_id=?',(chat_id, ))
#         user.current_post_id = cur.fetchone()[0]
#         if media:
#             cur.execute('INSERT INTO home_postmedia (POST_ID,MEDIA_1,MEDIA_2,MEDIA_3,MEDIA_4,MEDIA_5,MEDIA_6,MEDIA_7,MEDIA_8,MEDIA_9)'
#                 ' VALUES(?,?,?,?,?,?,?,?,?,?)',(
#                     user.current_post_id, user.media[1], user.media[2], user.media[3], user.media[4],
#                     user.media[5], user.media[6], user.media[7], user.media[8], user.media[9],
#                     )
#             )
#             conn.commit()
#         elif location:

#             cur.execute('INSERT INTO home_postlocation (POST_ID,LATITUDE,LONGITUDE)'
#                 ' VALUES(?,?,?)',
#             (
#                 user.current_post_id, user.location[1], user.location[2],
#             )
#             )
#             conn.commit()
#         cur.close()
#         conn.close()
#         user.unpublished_posts[user.current_post_id] = post_date
#         user.unpublished_posts_reverse[post_date] = user.current_post_id
#         return user
    

#     def make_published():
#         conn = sqlite3.connect(DATABASE_PATH)
#         cur = conn.cursor()
#         cur.execute("UPDATE home_post SET PUBLISHED = ? WHERE id= ? ", (True, user.current_post_id, ))
#         conn.commit()
#         cur.close()
#         conn.close() 
    
#     if user.save_post and not user.publish:
#         user = save(user)
#         user = cancel_post(user)
#     elif not user.save_post and user.publish:
#         try:
#             show_created_post(
#                 user, user.current_channel,
#                 bot = bot, update = update,
#                 context = CallbackContext
#                 )
#         except:
#             show_created_post(
#                 user, update.message.chat_id,
#                 bot = bot, update = update,
#                 context = CallbackContext
#                 )
#             make_published()
#             user = save(user)
            
            
#     user.save_post = False
#     return user


# def find_post(user, post_date):
#     user.show_unpublished_posts = False
#     user.event[0] = True
#     user.date = post_date
#     user.current_post_id = user.unpublished_posts_reverse[post_date]
#     conn = sqlite3.connect(DATABASE_PATH)
#     cur = conn.cursor()
#     cur.execute("SELECT * from home_post WHERE id=?",
#                 (user.current_post_id, ))
#     post_data = cur.fetchall()[0]
#     user.text[1] = post_data[2]

#     if post_data[4]:
#         # media
#         cur.execute("SELECT * from home_postmedia WHERE post_id=?",
#                     (user.current_post_id, ))
#         try:
#             media = cur.fetchall()[0]
#             for i in enumerate(media[1:-1]):
#                 user.media[i[0] + 1] = i[1]
#         except:
#             pass
#     if post_data[5]:
#         # location
#         cur.execute("SELECT * from home_postlocation WHERE post_id=?",
#                     (user.current_post_id, ))
#         try:
#             location = cur.fetchall()[0]
#             user.location[1] = location[1]  # latitude
#             user.location[2] = location[2]  # longitude
#         except:
#             pass
#     return user


# def update_post(user, chat_id, bot: Bot, update: Update, context=CallbackContext):


#     def update():
#         conn = sqlite3.connect(DATABASE_PATH)
#         cur = conn.cursor()
#         cur.execute('UPDATE home_post set POST_TEXT=?, LOCATION=?, MEDIA=? WHERE ID= ?',(user.text[1], True, True, user.current_post_id))
#         conn.commit()
        
#         if not cur.execute("SELECT * from home_postmedia WHERE post_id=?", (user.current_post_id, )).fetchall():
#             cur.execute('INSERT INTO home_postmedia (POST_ID,MEDIA_1,MEDIA_2,MEDIA_3,MEDIA_4,MEDIA_5,MEDIA_6,MEDIA_7,MEDIA_8,MEDIA_9)'
#                         ' VALUES(?,?,?,?,?,?,?,?,?,?)', (
#                             user.current_post_id, user.media[1], user.media[2], user.media[3], user.media[4],
#                             user.media[5], user.media[6], user.media[7], user.media[8], user.media[9],
#                         )
#                         )
#         else:
#             cur.execute('UPDATE  home_postmedia set MEDIA_1=?,MEDIA_2=?,MEDIA_3=?,MEDIA_4=?,MEDIA_5=?,MEDIA_6=?,MEDIA_7=?,MEDIA_8=?,MEDIA_9=?'
#                         ' where post_id=?', (
#                             user.media[1], user.media[2], user.media[3], user.media[4],
#                             user.media[5], user.media[6], user.media[7], user.media[8], 
#                             user.media[9], user.current_post_id
#                         )
#                         )
#         conn.commit()
    
#         if not cur.execute("SELECT * from home_postlocation WHERE post_id=?",(user.current_post_id, )).fetchall():
#             cur.execute(
#                 'INSERT INTO home_postlocation (POST_ID,LATITUDE,LONGITUDE) VALUES(?,?,?)', (user.current_post_id, user.location[1], user.location[2]))
#         else:
#             cur.execute('UPDATE  home_postlocation set LATITUDE=?,LONGITUDE=?'
#                         ' where post_id=?', (user.location[1], user.location[2], user.current_post_id))
#             conn.commit()
#         cur.close()
#         conn.close()
    

#     def make_published():
#         conn = sqlite3.connect(DATABASE_PATH)
#         cur = conn.cursor()
#         cur.execute("UPDATE home_post SET PUBLISHED = ? WHERE id= ? ",
#                     (True, user.current_post_id, ))
#         conn.commit()
#         cur.close()
#         conn.close()
        
#     if user.update_post and not user.publish:
#         update()
#         user = cancel_post(user)
#     elif user.update_post and user.publish:
#         update()
#         user = show_created_post(
#             user, user.chat_id,
#             bot=bot, update=update,
#             context=CallbackContext
#         )
#         try:
#             del user.unpublished_posts[user.current_post_id]
#             del user.unpublished_posts_reverse[user.date]
#         except:
#             pass      
#         make_published()
#         user = cancel_post(user)
#     user.update = False
#     return user
