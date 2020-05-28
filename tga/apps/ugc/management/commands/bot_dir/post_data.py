from .translates import translates
from telegram import ReplyKeyboardRemove
from telegram import Bot, Update, Location, InputMediaPhoto, InputMediaVideo
try:
	from .keyboards import LANGUAGE_EN, LANGUAGE_RU, \
		start_keyboard, conifrm_keyboard, post_keyboard, language_keyboard, email_keyboard, \
		regisration_keyboard, channels_keyboard, unpublished_keyboard, find_post_keyboard, \
		help_keyboard, start_page_keyboard
except ImportError:
	pass

class Post:

    
    def __init__(
            self, post_id, created_at, 
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
        self.publish = False
        
        self.save_post = False
        self.update_post = False
        
        self.show_unpublished_posts = False
        self.all_channels = False
        
    
    def add_text(self, update, user):
        user.post.text[0] = False
        user.post.text[1] = user.data
        update.effective_chat.send_message(
                text=translates[user.language]['I got text'],
                reply_markup=post_keyboard(user),
                )
    
    
    
    def send_post(self, update, user, context, chat_id):
        text = self.text[1]
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
                            text)
                            )
                    else:
                        media.append(InputMediaPhoto(
                            user.post.media[i][1:],)
                            )
                elif test[0] == 'v':
                    if len(media) == 0:
                        media.append(InputMediaVideo(
                            user.post.media[i][1:],
                            text)
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
            if user.media[1][0] == 'p':
                context.bot.send_photo(
                    chat_id=chat_id,
                    caption=text,
                    photo=user.post.media[1][1:],
                    )
            else:
                context.bot.send_video(
                    chat_id=chat_id,
                    caption=text,
                    video=user.post.media[1][1:],
                    )
        if len(media) == 0:
            context.bot.send_message(
                chat_id=chat_id,
                text=text,
            )
        
        # if len(user.channels) > 0:
        #     if user.all_channels:
        #         for i in user.channels:
        #             send_post(i)
        #             sleep(1)
        #         user.all_channels = False
        #     else:
        #         send_post(chat_id)
        # else:
        #     send_post(chat_id)
    
    
    def show_post(self, update, user, context):
        if user.update_and_publish:
            pass
        elif user.save_and_publish:
            pass
        else:
            self.send_post(update, user, context, user.chat_id)
        