from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ReplyKeyboardRemove
from telegram.utils.request import Request

from django.core.management.base import BaseCommand
from django.conf import settings

from ugc.models import Profile

from email_validator import validate_email, EmailNotValidError

from logging import getLogger
from random import randint

from .bot_dir.utils import debug_requests
from .bot_dir.config import Settings, User, User_params, load_config
from .bot_dir.translates import translates
from .bot_dir.functions import take_users, take_user_data, cancel_post,\
    add_user_to_database, location_for_post, media_for_post, \
    text_for_post, show_created_post, save_post, \
    create_post_button, change_language, update_post, \
    send_email, remove_channel, add_channel, \
    find_post, take_emails
from .bot_dir.keyboards import LANGUAGE_EN, LANGUAGE_RU, \
    start_keyboard, conifrm_keyboard, post_keyboard, language_keyboard, email_keyboard, \
    regisration_keyboard, channels_keyboard, unpublished_keyboard, find_post_keyboard, \
   	help_keyboard


config = load_config()
logger = getLogger(__name__)
settings = Settings()
user = User()


@debug_requests
def do_start(bot: Bot, update: Update, context=CallbackContext):
	chat_id = update.message.chat_id
	if len(settings.users) == 0 and settings.request_count == 0:
		settings.request_count += 1
		settings.users, settings.emails = take_users(), take_emails()
	if chat_id not in user.user:
		user.user[chat_id] = User_params()
		if chat_id not in settings.users:
			bot.send_message(
				chat_id=chat_id,
				text='Select language / Выберите язык',
				reply_markup=language_keyboard(user.user[chat_id]),
			)
		else:
			take_user_data(user.user[chat_id], chat_id)
			bot.send_message(
				chat_id=update.message.chat_id,
				text=translates[user.user[chat_id].language]['Hello'] +
				user.user[chat_id].username,
				reply_markup=start_keyboard(user.user[chat_id]),
				)
	else:
		if chat_id not in settings.users and not user.user[chat_id].check_email:
			user.user[chat_id].check_email = True
			bot.send_message(
				chat_id=update.message.chat_id,
				text=translates[user.user[chat_id].language]['Tap email'],
				)


@debug_requests
def take_text(bot: Bot, update: Update, context=CallbackContext):
	chat_id = update.message.chat_id
	if chat_id in user.user:
		user.user[chat_id].data = update.message.text
		if user.user[chat_id].check_email:
			user.user[chat_id].email = user.user[chat_id].data
			try:
				validation = validate_email(user.user[chat_id].email)
				bot.send_message(
					chat_id=chat_id,
					text=translates[user.user[chat_id].language]['check_email'],
					reply_markup=email_keyboard(user.user[chat_id]),
				)
				user.user[chat_id].check_email = False
				user.user[chat_id].access = True
			except EmailNotValidError:
				bot.send_message(
				chat_id=chat_id,
				text=translates[user.user[chat_id].language]['tap_correct_email'],
				reply_markup=ReplyKeyboardRemove(),
				)
		if not user.user[chat_id].check_email and  user.user[chat_id].language != '' and user.user[chat_id].data == translates[user.user[chat_id].language]["tap email again"]:
			user.user[chat_id].check_email = True
			bot.send_message(
				chat_id=chat_id,
				text=translates[user.user[chat_id].language]['send_email_again'],
				reply_markup=ReplyKeyboardRemove(),
				)
		if user.user[chat_id].data == LANGUAGE_EN:
			if user.user[chat_id].language == '':
				user.user[chat_id].language = 'EN'
				bot.send_message(
				    chat_id=update.message.chat_id,
				    text='Language was successfully selected',
					reply_markup=ReplyKeyboardRemove(),
					)
			else:
				if user.user[chat_id].user_registration:
					user.user[chat_id] = change_language(user.user[chat_id], chat_id, 'EN')
					user.user[chat_id].language = 'EN' 
					bot.send_message(
						chat_id=update.message.chat_id,
						text='Language was successfully changed',
						reply_markup=start_keyboard(user.user[chat_id]),
						)
			return do_start(bot=bot, update=update, context=context)
		elif user.user[chat_id].data == LANGUAGE_RU:
			if user.user[chat_id].language == '':
				user.user[chat_id].language = 'RU'
				bot.send_message(
				    chat_id=update.message.chat_id,
				    text='Язык успешно выбран',
					reply_markup=ReplyKeyboardRemove(),
					)		
			else:
				if user.user[chat_id].user_registration:
					user.user[chat_id] = change_language(user.user[chat_id], chat_id, 'RU')
					user.user[chat_id].language = 'RU'
					bot.send_message(
						chat_id=update.message.chat_id,
						text='Язык успешно изменён',
						reply_markup=start_keyboard(user.user[chat_id]),
						)
			return do_start(bot=bot, update=update, context=context)
		if user.user[chat_id].access:
			if user.user[chat_id].data == translates[user.user[chat_id].language]["BUTTON_SEND_CODE"]:
				user.user[chat_id].access = False
				user.user[chat_id].code[1] = True
				user.user[chat_id].code[0] = randint(100000,1000000)
				bot.send_message(
					chat_id=update.message.chat_id,
					text=translates[user.user[chat_id].language]["Code_has_been_sent"],
					reply_markup=ReplyKeyboardRemove(),
					)
				return send_email(user.user[chat_id])
		if user.user[chat_id].get_name:
			if user.user[chat_id].data != translates[user.user[chat_id].language]["REGISTER_ME"]:
				user.user[chat_id].username = user.user[chat_id].data	
				bot.send_message(
					chat_id= chat_id,
					text=translates[user.user[chat_id].language]["i_got_name"],
					reply_markup=regisration_keyboard(user.user[chat_id]),
					)		
			else:
				if user.user[chat_id].username != False:
					add_user_to_database(settings, user.user[chat_id], chat_id)
					p = Profile(
						name=user.user[chat_id].username,
						external_id=update.message.chat_id,
						email=user.user[chat_id].email,
					)
					p.save_base()
					bot.send_message(
						chat_id=chat_id,
						text=f'Welcome {user.user[chat_id].username}',
						reply_markup=start_keyboard(user.user[chat_id])
						)
		if user.user[chat_id].code[1]:
			try:
				if int(user.user[chat_id].data) == user.user[chat_id].code[0]:
					bot.send_message(
						chat_id= chat_id,
						text='Well done.\n'+ 
						translates[user.user[chat_id].language]['Name to sign up'],
						)
					user.user[chat_id].get_name = True
					user.user[chat_id].code[1] = False
				else:
					bot.send_message(
						chat_id= chat_id,
						text=translates[user.user[chat_id].language]['wrong_code'],
					)
			except ValueError:
				bot.send_message(
					chat_id= chat_id,
					text=translates[user.user[chat_id].language]['wrong_code'],
					)		
		if user.user[chat_id].user_registration:
			if user.user[chat_id].data == translates[user.user[chat_id].language]['BUTTON3_BOT_HELP']:
				user.user[chat_id].help = True
				bot.send_message(
					chat_id=update.message.chat_id,
					text=translates[user.user[chat_id].language]['help_text'],
					reply_markup=help_keyboard(user.user[chat_id]),
				)
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['how_to_create']:
				if user.user[chat_id].help:
						bot.send_message(
						chat_id=update.message.chat_id,
						text=translates[user.user[chat_id].language]['create_guide'],
						reply_markup=help_keyboard(
							user.user[chat_id]),
                        )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['how_to_update']:
				if user.user[chat_id].help:
						bot.send_message(
						chat_id=update.message.chat_id,
						text=translates[user.user[chat_id].language]['update_guide'],
						reply_markup=help_keyboard(
							user.user[chat_id]),
                        )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['text_guide']:
				if user.user[chat_id].help:
						bot.send_message(
						chat_id=update.message.chat_id,
						text=translates[user.user[chat_id].language]['text_usage'],
						reply_markup=help_keyboard(
							user.user[chat_id]),
                        )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['location_guide']:
				if user.user[chat_id].help:
						bot.send_message(
						chat_id=update.message.chat_id,
						text=translates[user.user[chat_id].language]['location_usage'],
						reply_markup=help_keyboard(
							user.user[chat_id]),
                        )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['media_guide']:
				if user.user[chat_id].help:
						bot.send_message(
						chat_id=update.message.chat_id,
                                                    text=translates[user.user[chat_id].language]['media_usage'],
						reply_markup=help_keyboard(
							user.user[chat_id]),
                        )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['media_guide']:
				if user.user[chat_id].help:
						bot.send_message(
						chat_id=update.message.chat_id,
                                                    text=translates[user.user[chat_id].language]['media_usage'],
						reply_markup=help_keyboard(
							user.user[chat_id]),
                        )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['work_with_channels']:
				if user.user[chat_id].help:
						bot.send_message(
						chat_id=update.message.chat_id,
                        text=translates[user.user[chat_id].language]['channels_usage'],
						reply_markup=help_keyboard(
							user.user[chat_id]),
                        )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['BUTTON4_CREATE_POST']:
				user.user[chat_id].add_channel = False
				user.user[chat_id].remove_channel = False
				user.user[chat_id].help = False
				return create_post_button(
					user.user[chat_id], chat_id,
					bot=bot, update=update
					)
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['START_PAGE']:
				user.user[chat_id] = cancel_post(user.user[chat_id])
				bot.send_message(
					chat_id=chat_id,
					text=translates[user.user[chat_id].language]['welcome'],
					reply_markup=start_keyboard(user.user[chat_id]),
				)

			elif user.user[chat_id].data == translates[user.user[chat_id].language]['list_of_channels']:
			    bot.send_message(
			        chat_id=chat_id,
			        text='Your channels list',
			        reply_markup=channels_keyboard(user.user[chat_id]),
			    )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['CHANGE_LANGUAGE']:
			    user.user[chat_id].change_language = True
			    bot.send_message(
			        chat_id=chat_id,
			        text='Select language / Выберите язык',
			        reply_markup=language_keyboard(user.user[chat_id]),
			    )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['BUTTON10_CANCEL_POST']:
			    if user.user[chat_id].event[0]:
				    user.user[chat_id].text[0] = False
				    user.user[chat_id].location[0] = False
				    user.user[chat_id].media[0] = False
				    bot.send_message(
				        chat_id=update.message.chat_id,
				        text=translates[user.user[chat_id].language]['Need confirmation'],
				        reply_markup=conifrm_keyboard(user.user[chat_id])
				    )
				    user.user[chat_id].event[1] = True
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['DELETE_LOCATION']:
				if user.user[chat_id].event[0]:
					user.user[chat_id].location = [False, '', '']
					bot.send_message(
				        chat_id=update.message.chat_id,
				        text=translates[user.user[chat_id].language]['location_deleted'],
				        reply_markup=post_keyboard(user.user[chat_id])
				    )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['DELETE_TEXT']:
				if user.user[chat_id].event[0]:
					user.user[chat_id].text = [False, '']
					bot.send_message(
				        chat_id=update.message.chat_id,
				        text=translates[user.user[chat_id].language]['text_deleted'],
				        reply_markup=post_keyboard(user.user[chat_id])
				    )  
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['CONFIRM_YES']:
			    if user.user[chat_id].event[1]:
			        cancel_post(user.user[chat_id])
			        bot.send_message(
			            chat_id=chat_id,
			            text=translates[user.user[chat_id].language]['Post_canceled'],
			            reply_markup=start_keyboard(user.user[chat_id])
			        )
			    if user.user[chat_id].remove_channel:
			    	remove_channel(user.user[chat_id], chat_id)
			    	user.user[chat_id].remove_channel = False
			    	user.user[chat_id].current_channel = ''
			    	bot.send_message(
					    chat_id=chat_id,
					    text=translates[user.user[chat_id].language]['channel_removed'],
					    reply_markup=start_keyboard(user.user[chat_id])
					)
			    if user.user[chat_id].add_channel:
			    	add_channel(user.user[chat_id], chat_id)
			    	user.user[chat_id].add_channel = False
			    	user.user[chat_id].current_channel = ''
			    	bot.send_message(
					    chat_id=chat_id,
					    text=translates[user.user[chat_id].language]['channel_added'],
					    reply_markup=start_keyboard(user.user[chat_id])
					)
				
			elif user.user[chat_id].data\
			== translates[user.user[chat_id].language]['CONFIRM_NO']:
			    if user.user[chat_id].event[1]:
			        user.user[chat_id].event[1] = False
			        bot.send_message(
			            chat_id=chat_id,
			            text=translates[user.user[chat_id].language]['continue_post'],
			            reply_markup=post_keyboard(user.user[chat_id])
			        )
			    if user.user[chat_id].remove_channel:
			    	user.user[chat_id].remove_channel = False
			    	user.user[chat_id].current_channel = ''
			    	bot.send_message(
					    chat_id=chat_id,
					    text=translates[user.user[chat_id].language]['action_canсeled'],
					    reply_markup=start_keyboard(user.user[chat_id])
					) 
			    if user.user[chat_id].add_channel:
			    	user.user[chat_id].add_channel = False
			    	user.user[chat_id].current_channel = ''
			    	bot.send_message(
					    chat_id=chat_id,
					    text=translates[user.user[chat_id].language]['action_canсeled'],
					    reply_markup=start_keyboard(user.user[chat_id])
					)
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['update_post']:
				if user.user[chat_id].event[0]:					
					user.user[update.message.chat_id].update_post = True
					update_post(
						user.user[chat_id], chat_id,
						bot=bot, update=update, context=context,
						)
					bot.send_message(
						chat_id=chat_id,
						text=translates[user.user[chat_id].language]['updated'],
						reply_markup=start_keyboard(user.user[chat_id]),
					        )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['BUTTON5_TEXT_FOR_POST']:
				if user.user[chat_id].event[0]:
					bot.send_message(
							chat_id=chat_id,
							text=translates[user.user[chat_id]
											.language]['Tap text for post'],
							reply_markup=post_keyboard(user.user[chat_id]),
						)
					return text_for_post(user.user[chat_id])
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['BUTTON6_ADD_LOCATION']:
			    if user.user[chat_id].event[0]:
			        bot.send_message(
			            chat_id=chat_id,
			            text=translates[user.user[chat_id].language]['Send location'],
			            reply_markup=post_keyboard(user.user[chat_id]),
			            )
			        return location_for_post(user.user[chat_id])
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['BUTTON7_ADD_MEDIA']:
			    if user.user[chat_id].event[0]:
			        bot.send_message(
			            chat_id=chat_id,
			            text=translates[user.user[chat_id].language]['Send media'],
			            reply_markup=post_keyboard(user.user[chat_id]),
			            )
			        return media_for_post(user.user[chat_id])
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['BUTTON8_SHOW_POST']:
			    if user.user[chat_id].event[0]:
			        if any(\
			        	[user.user[update.message.chat_id].text[1],\
			        	user.user[update.message.chat_id].media[1],\
			        	user.user[update.message.chat_id].location[1]]\
			        	):
			            return show_created_post(
			                user.user[chat_id], chat_id,
			                bot=bot, update=update, context=context
			                )
			        else:
			            bot.send_message(
			                chat_id=chat_id,
			                text=translates[user.user[chat_id].language]['nothing_to_show'],
			                reply_markup=post_keyboard(user.user[chat_id])
			                )
			
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['BUTTON9_SAVE_POST']:
			    if user.user[chat_id].event[0]:
			    	if not any([user.user[update.message.chat_id].text[1], user.user[update.message.chat_id].media[1], user.user[update.message.chat_id].location[1]]):
			        	bot.send_message(
			        		chat_id=chat_id,
			        		text='Nothing to save',
			        		reply_markup=post_keyboard(user.user[chat_id])
			        		) 
			    	elif any([user.user[update.message.chat_id].text[1], user.user[update.message.chat_id].media[1], user.user[update.message.chat_id].location[1]]):
				        user.user[update.message.chat_id].save_post = True
				        save_post(
				            user.user[chat_id], chat_id,
				            bot=bot, update=update, context=context
				            )
				        bot.send_message(
					        chat_id=chat_id,
					        text=translates[user.user[chat_id].language]['Done'],
					        reply_markup=start_keyboard(user.user[chat_id]),
					        )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['publish_and_save']:
			    if user.user[chat_id].event[0]:
			    	if not any([user.user[update.message.chat_id].text[1], user.user[update.message.chat_id].media[1], user.user[update.message.chat_id].location[1]]):
			        	bot.send_message(
			        		chat_id=chat_id,
			        		text='Nothing to save',
			        		reply_markup=post_keyboard(user.user[chat_id])
			        		) 
			    	elif any([user.user[update.message.chat_id].text[1], user.user[update.message.chat_id].media[1], user.user[update.message.chat_id].location[1]]):
				        user.user[update.message.chat_id].text[0] = False 
				        user.user[update.message.chat_id].save_post = True
				        user.user[chat_id].publish = True
				        save_post(
				            user.user[chat_id], update.message.chat_id,
				            bot=bot, update=update, context=context
				            )
				        bot.send_message(
					        chat_id=update.message.chat_id,
					        text=translates[user.user[chat_id].language]['Done'],
					        reply_markup=channels_keyboard(user.user[chat_id]),
					        )
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['publish_and_update']:
				if user.user[chat_id].event[0]:
					if not any([user.user[update.message.chat_id].text[1], user.user[update.message.chat_id].media[1], user.user[update.message.chat_id].location[1]]):
						bot.send_message(
			        		chat_id=chat_id,
			        		text='Nothing to update',
			        		reply_markup=post_keyboard(user.user[chat_id])
			        		)
					elif any([user.user[update.message.chat_id].text[1], user.user[update.message.chat_id].media[1], user.user[update.message.chat_id].location[1]]):
						user.user[update.message.chat_id].text[0] = False 
						user.user[update.message.chat_id].update_post = True
						user.user[chat_id].publish = True
						bot.send_message(
							chat_id=update.message.chat_id,
							text=translates[user.user[update.message.chat_id].language]['Done'],
							reply_markup=channels_keyboard(user.user[update.message.chat_id]),
							)
			if user.user[chat_id].publish and user.user[chat_id].data in user.user[chat_id].channels:
				user.user[chat_id].current_channel = user.user[chat_id].data
				return save_post(
					user.user[chat_id], chat_id,
					bot=bot, update=update,
					context=context
					)
			if user.user[chat_id].publish and user.user[chat_id].data == translates[user.user[chat_id].language]['ALL_CHANNELS']:
				user.user[chat_id].all_channels = True
				if user.user[chat_id].update_post:
					user.user[chat_id] = update_post(
						user.user[chat_id], chat_id,
						bot=bot, update=update,
						context=context
					)
					bot.send_message(
						chat_id=chat_id,
						text='Starting to post in all your accesseble channels',
						reply_markup=start_keyboard(user.user[chat_id])
					)
					user.user[chat_id] = cancel_post(user.user[chat_id])
				else:
					save_post(
						user.user[chat_id], chat_id,
						bot=bot, update=update,
						context=context
					)
					bot.send_message(
						chat_id=chat_id,
						text='Starting to post in all your accesseble channels',
						reply_markup=start_keyboard(user.user[chat_id])
						)
				return do_start(bot=bot, update=update, context=context)
			elif user.user[chat_id].data == translates[user.user[chat_id].language]['show_posts']:
				if len(user.user[chat_id].unpublished_posts) > 0:
					user.user[chat_id].show_unpublished_posts = True
					bot.send_message(
						chat_id=chat_id, 
						text='Select post', 
						reply_markup=unpublished_keyboard(user.user[chat_id])
						)
					return True
				else:
					bot.send_message(
			    		chat_id=chat_id,
			    		text='All your posts already published',
			    		reply_markup=start_keyboard(user.user[chat_id])
			    		)
			if user.user[chat_id].remove_channel:
				user.user[chat_id].current_channel = user.user[chat_id].data
				bot.send_message(
					chat_id=chat_id,
					text='Confirm please',
					reply_markup=conifrm_keyboard(user.user[chat_id]),
					)
			if user.user[chat_id].show_unpublished_posts:
				user.user[chat_id] = find_post(user.user[chat_id], user.user[chat_id].data)
				user.user[chat_id].unpublished_keyboard = True
				bot.send_message(
					chat_id=chat_id,
					text='You can edit your post',
					reply_markup=find_post_keyboard(user.user[chat_id]),
				)
			if user.user[chat_id].add_channel:
				if user.user[chat_id].data != translates[user.user[chat_id].language]['remove_channel']:
					if user.user[chat_id].data not in user.user[chat_id].channels and\
					'@' + user.user[chat_id].data not in user.user[chat_id].channels:
						if '@' in user.user[chat_id].data:
							user.user[chat_id].current_channel = user.user[chat_id].data
						else:
							user.user[chat_id].current_channel = '@' + user.user[chat_id].data
						bot.send_message(
							chat_id=chat_id,
							text='Confirm please',
							reply_markup=conifrm_keyboard(user.user[chat_id]),
							)
					else:
						user.user[chat_id].add_channel = False
						bot.send_message(
							chat_id=chat_id,
							text='This channel already exists',
							reply_markup=start_keyboard(user.user[chat_id]),
							)
				else:
					user.user[chat_id].remove_channel = True
					user.user[chat_id].add_channel = False
					bot.send_message(
						chat_id=chat_id,
						text='Select channel',
						reply_markup=channels_keyboard(user.user[chat_id]),
						)
					return True
			if not user.user[chat_id].event[0]:
				if user.user[chat_id].data == translates[user.user[chat_id].language]['add_channel']:
					if '@' in user.user[chat_id].data:
						user.user[chat_id].current_channel = user.user[chat_id].data
					else:
						user.user[chat_id].current_channel = '@' + user.user[chat_id].data
					user.user[chat_id].add_channel = True
					user.user[chat_id].remove_channel = False
					bot.send_message(
						chat_id=chat_id,
						text='Send channel id\n(You can send without @)',
						)
				elif user.user[chat_id].data == translates[user.user[chat_id].language]['remove_channel'] and user.user[chat_id].add_channel is False:
					if len(user.user[chat_id].channels) > 0:
						user.user[chat_id].remove_channel = True
						user.user[chat_id].add_channel = False
						bot.send_message(
							chat_id=chat_id,
							text='Select channel',
							reply_markup=channels_keyboard(user.user[chat_id]),
							)
					else:
						bot.send_message(
							chat_id=chat_id,
							text='You have no channels',
							reply_markup=start_keyboard(user.user[chat_id]),
							)
			if user.user[chat_id].text[0]:
				user.user[chat_id].text[0] = False
				if user.user[chat_id].event[0]:
					if any([user.user[chat_id].text[0], user.user[chat_id].location[0]]):
						bot.send_message(
								chat_id=chat_id,
								text=translates[user.user[chat_id]
												.language]['send_correct_data'],
								reply_markup=post_keyboard(user.user[chat_id]),
							)
					else:
						user.user[chat_id].text[1] = user.user[chat_id].data
						bot.send_message(
								chat_id=chat_id,
								text=translates[user.user[chat_id].language]['I got text'],
								reply_markup=post_keyboard(user.user[chat_id]),
						)
			if user.user[chat_id].media[0]:
			    try:
			        if type(int(user.user[chat_id].data.strip())) is int:
			                i = int(user.user[chat_id].data.strip())
			                if i != 0:
			                    if user.user[chat_id].media[i] != '':
			                        bot.send_message(
			                            chat_id=chat_id,
			                            text=translates[user.user[chat_id].language]["Item removed"],
			                        )
			                        user.user[chat_id].media[i] = ''
			                    else:
			                        bot.send_message(
			                            chat_id=chat_id,
			                            text=translates[user.user[chat_id].language]["Wrong number"],
			                        )
			        else:
			            bot.send_message(
			                chat_id=update.message.chat_id,
			                text=translates[user.user[chat_id].language]["Send correct message"],
			            )
			    except ValueError:
			    	pass
	else:
		do_start(bot=bot, update=update, context=context)
		take_text(bot=bot, update=update, context=context)


@debug_requests
def get_media(bot: Bot, update: Update):
	chat_id = update.message.chat_id
	if chat_id in user.user:
		if any([user.user[chat_id].text[0], user.user[chat_id].location[0]]):
			bot.send_message(
				chat_id=chat_id,
				text=translates[user.user[chat_id]
								.language]['send_correct_data'],
				reply_markup=post_keyboard(user.user[chat_id]),
			)
		else:
			if user.user[update.message.chat_id].media[0]:
				user.user[update.message.chat_id].check_list = []
				for i in range(1, 10):
					if user.user[update.message.chat_id].media[i] == '':
						user.user[update.message.chat_id].check_list.append(i)
				if len(user.user[update.message.chat_id].check_list) > 0:
					try:
						user.user[update.message.chat_id].media_id[0] = update.message.photo[-1].file_id
					except:
						pass
					try:
						user.user[update.message.chat_id].media_id[1] = update.message.video.file_id
					except:
						pass
					if user.user[update.message.chat_id].media_id[0] != '':
						for i in range(1, 11):
							if user.user[update.message.chat_id].media[i] == '':
								user.user[update.message.chat_id].media[i] = 'p' + user.user[update.message.chat_id].media_id[0]
								# 1st 'p' is photo detecter
								bot.send_message(
									chat_id=update.message.chat_id,
									text=translates[user.user[update.message.chat_id].language]["Accepted attachment № "] + str(i),
								)
								break
					if user.user[update.message.chat_id].media_id[1] != '':
						for i in range(1, 11):
							if user.user[update.message.chat_id].media[i] == '':
								user.user[update.message.chat_id].media[i] = 'v' + user.user[update.message.chat_id].media_id[1]
								# 1st 'v' is video detecter
								bot.send_message(
									chat_id=update.message.chat_id,
									text=translates[user.user[update.message.chat_id].language]["Accepted attachment № "] + str(i),
								)
								break
				else:
					bot.send_message(
						chat_id=update.message.chat_id,
						text=translates[user.user[update.message.chat_id].language]["attachment_limit"],
					)
	else:
		do_start(bot=bot, update=update, context=context)


@debug_requests
def get_location(bot: Bot, update: Update):
	chat_id = update.message.chat_id
	if chat_id in user.user:
		if any([user.user[chat_id].text[0], user.user[chat_id].media[0]]):
			bot.send_message(
				chat_id=chat_id,
				text=translates[user.user[chat_id]
								.language]['send_correct_data'],
				reply_markup=post_keyboard(user.user[chat_id]),
			)
		else:
			if user.user[chat_id].location[0]:
				user.user[chat_id].location.append(update.message.location)
				user.user[chat_id].location[1] = user.user[chat_id].location[3].latitude
				user.user[chat_id].location[2] = user.user[chat_id].location[3].longitude
				bot.send_message(
					chat_id=chat_id,
					text=translates[user.user[chat_id].language]['location_accepted'],
					reply_markup=post_keyboard(user.user[chat_id])
					)
	else:
		do_start(bot=bot, update=update, context=context)


def get_document(bot: Bot, update: Update):
	print('DOCUMENT')
	chat_id = update.message.chat_id
	if chat_id in user.user:
		if any([user.user[chat_id].text[0], user.user[chat_id].media[0], user.user[chat_id].location[0]]):
			bot.send_message(
				chat_id=chat_id,
				text=translates[user.user[chat_id]
								.language]['send_correct_data'],
				reply_markup=post_keyboard(user.user[chat_id]),
			)
	else:
		do_start(bot=bot, update=update, context=context)
	

def get_audio(bot: Bot, update: Update):
	chat_id = update.message.chat_id
	if chat_id in user.user:
		if any([user.user[chat_id].text[0], user.user[chat_id].media[0], user.user[chat_id].location[0]]):
			bot.send_message(
				chat_id=chat_id,
				text=translates[user.user[chat_id]
								.language]['send_correct_data'],
				reply_markup=post_keyboard(user.user[chat_id]),
			)
	else:
		do_start(bot=bot, update=update, context=context)



def get_voice(bot: Bot, update: Update):
	chat_id = update.message.chat_id
	if chat_id in user.user:
		if any([user.user[chat_id].text[0], user.user[chat_id].media[0], user.user[chat_id].location[0]]):
			bot.send_message(
				chat_id=chat_id,
				text=translates[user.user[chat_id]
								.language]['send_correct_data'],
				reply_markup=post_keyboard(user.user[chat_id]),
			)
	else:
		do_start(bot=bot, update=update, context=context)


class Command(BaseCommand):
	help = 'Telegram-bot'

	def handle(self, *args, **options):
		
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

		updater = Updater(
			bot=bot,
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
		document_message_handler = MessageHandler(
			Filters.document,
			get_document
		)
		audio_handler = MessageHandler(
			Filters.audio,
			get_audio,
		)
		voice_handler = MessageHandler(
			Filters.voice,
			get_voice,
		)
		updater.dispatcher.add_handler(start_handler)
		updater.dispatcher.add_handler(text_message_handler)
		updater.dispatcher.add_handler(img_message_handler)
		updater.dispatcher.add_handler(location_message_handler)
		updater.dispatcher.add_handler(video_message_handler)
		updater.dispatcher.add_handler(document_message_handler)
		updater.dispatcher.add_handler(audio_handler)
		updater.dispatcher.add_handler(voice_handler)
		updater.start_polling()
		updater.idle()
   
