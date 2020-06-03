# from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ReplyKeyboardRemove, Bot, Update
from telegram.utils.request import Request


from django.core.management.base import BaseCommand
from django.conf import settings


from logging import getLogger
from random import randint

from .bot_dir.utils import debug_requests
from .bot_dir.bot_data import BotState, load_config
from .bot_dir.user_data import UserObject
from .bot_dir.post_data import Post
from .bot_dir.translates import translates
try:
	from .bot_dir.functions import take_users, take_user_data, cancel_post,\
		add_user_to_database, location_for_post, media_for_post, \
		text_for_post, show_created_post, save_post, \
		create_post_button, change_language, update_post, \
		send_email, remove_channel, add_channel, \
		find_post, take_emails
except ImportError:
	pass
try:
	from .bot_dir.keyboards import LANGUAGE_EN, LANGUAGE_RU, \
		start_keyboard, conifrm_keyboard, post_keyboard, language_keyboard, email_keyboard, \
		regisration_keyboard, channels_keyboard, unpublished_keyboard, find_post_keyboard, \
		help_keyboard
except ImportError:
	pass


config = load_config()
logger = getLogger(__name__)
bot = BotState()



@debug_requests
def do_start(update: Update, context=CallbackContext):
	chat_id = update.message.chat_id
	if len(bot.users) == 0 and bot.request_count == 0:
		bot.request_count += 1
		bot.take_users()
		bot.take_emails()
	if chat_id not in bot.users:
		bot.users[chat_id] = UserObject(chat_id)
		if chat_id not in bot.users_ids:
			bot.users[chat_id].select_language = True
			update.effective_chat.send_message(
				text='Select language / Выберите язык',
				reply_markup=language_keyboard(bot.users[chat_id]),
			)
		else:
			bot.users[chat_id] = bot.take_user_data(bot.users[chat_id])
			update.effective_chat.send_message(
				text=translates[bot.users[chat_id].language]['Hello'] +
					bot.users[chat_id].username,
				reply_markup=start_keyboard(bot.users[chat_id]),
				)


@debug_requests
def take_text(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id
	if chat_id in bot.users:
		bot.users[chat_id].data = update.message.text

		if bot.users[chat_id].select_language:
			bot.users[chat_id].pick_language(update)
			return True
			

		if not bot.users[chat_id].user_registration:
			if bot.users[chat_id].check_email:
				bot.users[chat_id].email = bot.users[chat_id].data
				bot.users[chat_id].validate_user_email(update, bot.emails)
			elif bot.users[chat_id].language and bot.users[chat_id].data == translates[bot.users[chat_id].language]["send_email_again"]:
				bot.users[chat_id].check_email = True
				update.effective_chat.send_message(
					text=translates[bot.users[chat_id].language]['resend_email'],
					reply_markup=ReplyKeyboardRemove()
				)
			elif bot.users[chat_id].access:
				if bot.users[chat_id].data == translates[bot.users[chat_id].language]["BUTTON_SEND_CODE"]:
					bot.users[chat_id].create_code()
					bot.users[chat_id].send_email_with_code(update)
			elif bot.users[chat_id].code[1]:
				bot.users[chat_id].check_written_code(update)
			elif bot.users[chat_id].get_name:
				if bot.users[chat_id].data != translates[bot.users[chat_id].language]["REGISTER_ME"]:
					bot.users[chat_id].username = bot.users[chat_id].data
					update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]["i_got_name"],
						reply_markup=regisration_keyboard(bot.users[chat_id]),
					)
				else:
					if bot.users[chat_id].username != False:
						bot.users[chat_id].get_name = False
						bot.add_user_to_database(bot.users[chat_id])
						update.effective_chat.send_message(
							text=f'Welcome {bot.users[chat_id].username}',
							reply_markup=start_keyboard(bot.users[chat_id])
							)
			
			
				# bot.users[chat_id].post.add_text(update, bot.users[chat_id])
# 	# 			if bot.users[chat_id].event[0]:
# 	# 				bot.send_message(
# 	# 						chat_id=chat_id,
# 	# 						text=translates[bot.users[chat_id]
# 	# 										.language]['Tap text for post'],
# 	# 						reply_markup=post_keyboard(bot.users[chat_id]),
# 	# 					)
# 	# 				return text_for_post(bot.users[chat_id])
			
# 	# 		        return location_for_post(bot.users[chat_id])
# 	# 		
# 	# 		
		else:
			# add event check
			if bot.users[chat_id].data == translates[bot.users[chat_id].language]['BUTTON3_BOT_HELP']:
				bot.users[chat_id].clear_variables()
				update.effective_chat.send_message(
					text=translates[bot.users[chat_id].language]['help_text'],
					reply_markup=help_keyboard(bot.users[chat_id]),
				)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['how_to_create']:
				bot.users[chat_id].clear_variables()
				update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['create_guide'],
						reply_markup=help_keyboard(
							bot.users[chat_id]),
                        )
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['how_to_update']:
				bot.users[chat_id].clear_variables()
				update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['update_guide'],
						reply_markup=help_keyboard(
							bot.users[chat_id]),
                        )
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['text_guide']:
				bot.users[chat_id].clear_variables()
				update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['text_usage'],
						reply_markup=help_keyboard(
							bot.users[chat_id]),
                        )
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['location_guide']:
				bot.users[chat_id].clear_variables()
				update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['location_usage'],
						reply_markup=help_keyboard(
							bot.users[chat_id]),
                        )
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['media_guide']:
				bot.users[chat_id].clear_variables()
				update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['media_usage'],
						reply_markup=help_keyboard(
							bot.users[chat_id]),
                        )
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['media_guide']:
				bot.users[chat_id].clear_variables()
				update.effective_chat.send_message(
                        text=translates[bot.users[chat_id].language]['media_usage'],
						reply_markup=help_keyboard(
							bot.users[chat_id]),
                        )
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['work_with_channels']:
				bot.users[chat_id].clear_variables()
				update.effective_chat.send_message(
                        text=translates[bot.users[chat_id].language]['channels_usage'],
						reply_markup=help_keyboard(
							bot.users[chat_id]),
                        )
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['CHANGE_LANGUAGE']:
				bot.users[chat_id].clear_variables()
				bot.users[chat_id].select_language, bot.users[chat_id].change_language = True, True
				bot.users[chat_id].pick_language(update)
				update.effective_chat.send_message(
					text='Select language / Выберите язык',
					reply_markup=language_keyboard(bot.users[chat_id]),
				)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['START_PAGE']:
				bot.users[chat_id].clear_variables()
				# add creation check
				if bot.users[chat_id].post.saved:
					update.effective_chat.send_message(
						text='All post\'s data will be destroyed. Confirm action.',
						reply_markup=conifrm_keyboard(bot.users[chat_id]),
					)
					
				else:
					update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['welcome'],
						reply_markup=start_keyboard(bot.users[chat_id]),
					)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['add_channel'] or bot.users[chat_id].append_channel:
				bot.users[chat_id].clear_variables()
				bot.users[chat_id].append_channel = True
				bot.users[chat_id].add_channel(update, context=context)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['list_of_channels']:
				bot.users[chat_id].clear_variables()
				update.effective_chat.send_message(
					text=translates[bot.users[chat_id].language]['list_of_channels'],
					reply_markup=channels_keyboard(bot.users[chat_id]),
				)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['remove_channel'] or bot.users[chat_id].remove_channel:
				bot.users[chat_id].remove_channel = True
				bot.users[chat_id].delete_channel(update)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['BUTTON4_CREATE_POST']:
				bot.users[chat_id].clear_variables()
				bot.users[chat_id].create_post_button(update)
    
			elif bot.users[chat_id].post.text[0]:
				bot.users[chat_id].post.add_text(update, bot.users[chat_id])
    
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['BUTTON5_TEXT_FOR_POST']:
				if bot.users[chat_id].event[0]:
					bot.users[chat_id].post.text[0] = True
					update.effective_chat.send_message(
							text=translates[bot.users[chat_id].language]['Tap text for post'],
							reply_markup=post_keyboard(bot.users[chat_id]),
						)
				else:
					update.effective_chat.send_message(
							text='Press \'create post\' button before this action.',
							reply_markup=post_keyboard(bot.users[chat_id]),
						)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['DELETE_TEXT']:
				if bot.users[chat_id].event[0]:
					if bot.users[chat_id].post.text[1]:
						bot.users[chat_id].post.text[1] = ''
						update.effective_chat.send_message(
								text=translates[bot.users[chat_id].language]['text_deleted'],
								reply_markup=post_keyboard(bot.users[chat_id]),
							)
					else:
						update.effective_chat.send_message(
								text='There is no text to remove.',
								reply_markup=post_keyboard(bot.users[chat_id]),
							)
				else:
					update.effective_chat.send_message(
							text='Press \'create post\' button before this action.',
							reply_markup=post_keyboard(bot.users[chat_id]),
						)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['BUTTON8_SHOW_POST']:
				if bot.users[chat_id].event[0]:
					if any([bot.users[chat_id].post.text[1], bot.users[chat_id].post.media[1], bot.users[chat_id].post.location[1]]):
						bot.users[chat_id].post.show_post(update, bot.users[chat_id], context)
					else:
						update.effective_chat.send_message(
							text=translates[bot.users[chat_id].language]['nothing_to_show'],
							reply_markup=post_keyboard(bot.users[chat_id])
							)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['BUTTON6_ADD_LOCATION']:
				if bot.users[chat_id].event[0]:
					bot.users[chat_id].add_location = True
					update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['Send location'],
						reply_markup=post_keyboard(bot.users[chat_id]),
						)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['DELETE_LOCATION']:
				if bot.users[chat_id].event[0]:
					bot.users[chat_id].post.location = [False, '', '']
					update.effective_chat.send_message(
				        text=translates[bot.users[chat_id].language]['location_deleted'],
				        reply_markup=post_keyboard(bot.users[chat_id])
				    )
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['BUTTON7_ADD_MEDIA']:
				if bot.users[chat_id].event[0]:
					bot.users[chat_id].add_media = True
					update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['Send media'],
						reply_markup=post_keyboard(bot.users[chat_id]),
						)




# 	# 		
# 	# 		elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['update_post']:
# 	# 			if bot.users[chat_id].event[0]:					
# 	# 				bot.users[chat_id].update_post = True
# 	# 				update_post(
# 	# 					bot.users[chat_id], chat_id,
# 	# 					bot=bot, update=update, context=context,
# 	# 					)
# 	# 				bot.send_message(
# 	# 					chat_id=chat_id,
# 	# 					text=translates[bot.users[chat_id].language]['updated'],
# 	# 					reply_markup=start_keyboard(bot.users[chat_id]),
# 	# 				        )
# 	# 		
			# 
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['CONFIRM_YES']:
				if bot.users[chat_id].cancel_post:
					bot.users[chat_id].cancel_post = False
					bot.users[chat_id].post.clear_post()
					bot.users[chat_id].event = [False, False]
					update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['Post_canceled'],
						reply_markup=start_keyboard(bot.users[chat_id]),
					)
				if bot.users[chat_id].post.saved:
					bot.users[chat_id].post.clear_post()
					update.effective_chat.send_message(
						text='Post creation was finished. You were redirected on the start page.',
						reply_markup=start_keyboard(bot.users[chat_id]),
					)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['CONFIRM_NO']:
				if bot.users[chat_id].cancel_post:
					bot.users[chat_id].cancel_post = False
					update.effective_chat.send_message(
						text='You were returned to post creation',
						reply_markup=post_keyboard(bot.users[chat_id]),
					)
				if bot.users[chat_id].post.saved:
					update.effective_chat.send_message(
						text='You can select channel to send post',
						reply_markup=channels_keyboard(bot.users[chat_id]),
					)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['BUTTON9_SAVE_POST']:
				if bot.users[chat_id].event[0]:
					if not any([bot.users[chat_id].post.text[1], bot.users[chat_id].post.media[1], bot.users[chat_id].post.location[1]]):
						update.effective_chat.send_message(
							text='Nothing to save',
							reply_markup=post_keyboard(bot.users[chat_id])
							) 
					elif any([bot.users[chat_id].post.text[1], bot.users[chat_id].post.media[1], bot.users[chat_id].post.location[1]]):
						bot.users[chat_id] = bot.users[chat_id].post.save(bot.users[chat_id])
						# change text
						update.effective_chat.send_message(
							text=translates[bot.users[chat_id].language]['Done'],
							reply_markup=start_keyboard(bot.users[chat_id]),
							)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['BUTTON10_CANCEL_POST']:
				if bot.users[chat_id].event[0]:
					bot.users[chat_id].cancel_post = True
					update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['Need confirmation'],
						reply_markup=conifrm_keyboard(bot.users[chat_id]),
						)
				else:
					update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]['nothing_to_cancel']
					)
			elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['publish_and_save']:
				if bot.users[chat_id].event[0]:
					if not any([bot.users[chat_id].post.text[1], bot.users[chat_id].post.media[1], bot.users[chat_id].post.location[1]]):
						update.effective_chat.send_message(
							text='Nothing to save',
							reply_markup=post_keyboard(bot.users[chat_id])
							) 
					elif any([bot.users[chat_id].post.text[1], bot.users[chat_id].post.media[1], bot.users[chat_id].post.location[1]]):
						bot.users[chat_id].save_and_publish = True
						update.effective_chat.send_message(
							text='Select channel',
							reply_markup=channels_keyboard(bot.users[chat_id])
							)
      
# 	# 			        save_post(
# 	# 			            bot.users[chat_id], update.message.chat_id,
# 	# 			            bot=bot, update=update, context=context
# 	# 			            )
# 	# 			        bot.send_message(
# 	# 				        chat_id=update.message.chat_id,
# 	# 				        text=translates[bot.users[chat_id].language]['Done'],
# 	# 				        reply_markup=channels_keyboard(bot.users[chat_id]),
# 	# 				        )
# 	# 		elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['publish_and_update']:
# 	# 			if bot.users[chat_id].event[0]:
# 	# 				bot.users[chat_id].text[0] = False 
# 	# 				bot.users[chat_id].update_post = True
# 	# 				bot.users[chat_id].publish = True
# 	# 				bot.send_message(
# 	# 					chat_id=update.message.chat_id,
# 	# 					text=translates[bot.users[chat_id].language]['Done'],
# 	# 					reply_markup=channels_keyboard(bot.users[chat_id]),
# 	# 					)
# 	# 		if bot.users[chat_id].publish and bot.users[chat_id].data in bot.users[chat_id].channels:
# 	# 			bot.users[chat_id].current_channel = bot.users[chat_id].data
# 	# 			return save_post(
# 	# 				bot.users[chat_id], chat_id,
# 	# 				bot=bot, update=update,
# 	# 				context=context
# 	# 				)
# 	# 		if bot.users[chat_id].publish and bot.users[chat_id].data == translates[bot.users[chat_id].language]['ALL_CHANNELS']:
# 	# 			bot.users[chat_id].all_channels = True
# 	# 			if bot.users[chat_id].update_post:
# 	# 				bot.users[chat_id] = update_post(
# 	# 					bot.users[chat_id], chat_id,
# 	# 					bot=bot, update=update,
# 	# 					context=context
# 	# 				)
# 	# 				bot.send_message(
# 	# 					chat_id=chat_id,
# 	# 					text='Starting to post in all your accesseble channels',
# 	# 					reply_markup=start_keyboard(bot.users[chat_id])
# 	# 				)
# 	# 				bot.users[chat_id] = cancel_post(bot.users[chat_id])
# 	# 			else:
# 	# 				save_post(
# 	# 					bot.users[chat_id], chat_id,
# 	# 					bot=bot, update=update,
# 	# 					context=context
# 	# 				)
# 	# 				bot.send_message(
# 	# 					chat_id=chat_id,
# 	# 					text='Starting to post in all your accesseble channels',
# 	# 					reply_markup=start_keyboard(bot.users[chat_id])
# 	# 					)
# 	# 			return do_start(bot=bot, update=update, context=context)
# 	# 		elif bot.users[chat_id].data == translates[bot.users[chat_id].language]['show_posts']:
# 	# 			if len(bot.users[chat_id].unpublished_posts) > 0:
# 	# 				bot.users[chat_id].show_unpublished_posts = True
# 	# 				bot.send_message(
# 	# 					chat_id=chat_id, 
# 	# 					text='Select post', 
# 	# 					reply_markup=unpublished_keyboard(bot.users[chat_id])
# 	# 					)
# 	# 				return True
# 	# 			else:
# 	# 				bot.send_message(
# 	# 		    		chat_id=chat_id,
# 	# 		    		text='All your posts already published',
# 	# 		    		reply_markup=start_keyboard(bot.users[chat_id])
# 	# 		    		)
# 	# 		
# 	# 		if bot.users[chat_id].show_unpublished_posts:
# 	# 			bot.users[chat_id] = find_post(bot.users[chat_id], bot.users[chat_id].data)
# 	# 			bot.users[chat_id].unpublished_keyboard = True
# 	# 			# bot.users[chat_id].event[0] = True
# 	# 			bot.send_message(
# 	# 				chat_id=chat_id,
# 	# 				text='You can edit your post',
# 	# 				reply_markup=find_post_keyboard(bot.users[chat_id]),
# 	# 			)
# 	# 		if bot.users[chat_id].text[0]:
# 	# 			bot.users[chat_id].text[0] = False
# 	# 			if bot.users[chat_id].event[0]:
# 	# 				if any([bot.users[chat_id].text[0], bot.users[chat_id].location[0]]):
# 	# 					bot.send_message(
# 	# 							chat_id=chat_id,
# 	# 							text=translates[bot.users[chat_id]
# 	# 											.language]['send_correct_data'],
# 	# 							reply_markup=post_keyboard(bot.users[chat_id]),
# 	# 						)
# 	# 				else:
# 	# 					bot.users[chat_id].text[1] = bot.users[chat_id].data
# 	# 					bot.send_message(
# 	# 							chat_id=chat_id,
# 	# 							text=translates[bot.users[chat_id].language]['I got text'],
# 	# 							reply_markup=post_keyboard(bot.users[chat_id]),
# 	# 					)
			if bot.users[chat_id].save_and_publish:
				if bot.users[chat_id].data in bot.users[chat_id].channels:
					bot.users[chat_id].post.show_post(update, bot.users[chat_id], context)
				elif bot.users[chat_id].data == translates[bot.users[chat_id].language]["ALL_CHANNELS"]:
					pass
			try:
				if bot.users[chat_id].post.media[0]:
					try:
						if type(int(bot.users[chat_id].data.strip())) is int:
								i = int(bot.users[chat_id].data.strip())
								if i != 0:
									if bot.users[chat_id].post.media[i] != '':
										update.effective_chat.send_message(
											text=translates[bot.users[chat_id].language]["Item removed"],
										)
										bot.users[chat_id].post.media[i] = ''
									else:
										update.effective_chat.send_message(
											text=translates[bot.users[chat_id].language]["Wrong number"],
										)
						else:
							update.effective_chat.send_message(
								text=translates[bot.users[chat_id].language]["Send correct message"],
							)
					except ValueError:
						pass
			except AttributeError:
				pass
	else:
		do_start(update=update, context=context)
		# take_text(update=update, context=context)


@debug_requests
def get_media(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id
	if chat_id in bot.users:
		if any([bot.users[chat_id].post.text[0], bot.users[chat_id].add_location]):
			update.effective_chat.send_message(
				text=translates[bot.users[chat_id]
								.language]['send_correct_data'],
				reply_markup=post_keyboard(bot.users[chat_id]),
			)
		else:
			if bot.users[chat_id].add_media:
				bot.users[chat_id].check_list = []
				for i in range(1, 11):
					if bot.users[chat_id].post.media[i] == '':
						bot.users[chat_id].check_list.append(i)
				if len(bot.users[chat_id].check_list) > 0:
					try:
						bot.users[chat_id].post.media_id[0] = update.message.photo[-1].file_id
						bot.users[chat_id].post.media[0] = True
					except:
						pass
					try:
						bot.users[chat_id].post.media_id[1] = update.message.video.file_id
						bot.users[chat_id].post.media[0] = True
					except:
						pass
					if bot.users[chat_id].post.media_id[0] != '':
						for i in range(1, 11):
							if bot.users[chat_id].post.media[i] == '':
								bot.users[chat_id].post.media[i] = 'p' + bot.users[chat_id].post.media_id[0]
								# 1st 'p' is photo detecter
								update.effective_chat.send_message(
									text=translates[bot.users[chat_id].language]["Accepted attachment № "] + str(i),
								)
								break
					if bot.users[chat_id].post.media_id[1] != '':
						for i in range(1, 11):
							if bot.users[chat_id].post.media[i] == '':
								bot.users[chat_id].post.media[i] = 'v' + bot.users[chat_id].post.media_id[1]
								# 1st 'v' is video detecter
								update.effective_chat.send_message(
									text=translates[bot.users[chat_id].language]["Accepted attachment № "] + str(i),
								)
								break
				else:
					update.effective_chat.send_message(
						text=translates[bot.users[chat_id].language]["attachment_limit"],
					)
				
	else:
		do_start(update=update, context=context)
	


@debug_requests
def get_location(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id
	if chat_id in bot.users:
		if any([bot.users[chat_id].post.text[0], bot.users[chat_id].post.media[1]]):
			update.effective_chat.send_message(
				text=translates[bot.users[chat_id]
								.language]['send_correct_data'],
				reply_markup=post_keyboard(bot.users[chat_id]),
			)
		else:
			if bot.users[chat_id].add_location:
				location = update.message.location
				bot.users[chat_id].post.location[1] = location.latitude
				bot.users[chat_id].post.location[2] = location.longitude
				bot.users[chat_id].post.location[0] = True
				bot.users[chat_id].add_location = False
				update.effective_chat.send_message(
					text=translates[bot.users[chat_id].language]['location_accepted'],
					reply_markup=post_keyboard(bot.users[chat_id])
					)
	else:
		do_start(update=update, context=context)


@debug_requests
def get_document(update: Update, context=CallbackContext):
	chat_id = update.message.chat_id
	if chat_id in bot.users:
		if any([bot.users[chat_id].post.text[0], bot.users[chat_id].post.media[0], bot.users[chat_id].post.location[0]]):
			update.effective_chat.send_message(
				text=translates[bot.users[chat_id]
								.language]['send_correct_data'],
				reply_markup=post_keyboard(bot.users[chat_id]),
			)
	else:
		do_start(update, context)
	

@debug_requests
def get_audio(update: Update, context=CallbackContext):
	chat_id = update.message.chat_id
	if chat_id in bot.users:
		if any([bot.users[chat_id].post.text[0], bot.users[chat_id].post.media[0], bot.users[chat_id].post.location[0]]):
			update.effective_chat.send_message(
				text=translates[bot.users[chat_id].language]['send_correct_data'],
				reply_markup=post_keyboard(bot.users[chat_id]),
			)
	else:
		do_start(update, context)


class Command(BaseCommand):
	help = 'Telegram-bot'

	def handle(self, *args, **options):
		

		request = Request(
			connect_timeout=0.5,
			read_timeout=1.0,
		)
		
		bot = Bot(
			request=request,
			# token=bot.token, # production
			token='1086886864:AAH4iytj0B5KvpdFcf-N6akkuuAEOym7iG4', # development
		)
		updater = Updater(
			bot=bot,
			use_context=True
			)
		print(bot.get_me())
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
		updater.dispatcher.add_handler(start_handler)
		updater.dispatcher.add_handler(text_message_handler)
		updater.dispatcher.add_handler(img_message_handler)
		updater.dispatcher.add_handler(location_message_handler)
		updater.dispatcher.add_handler(video_message_handler)
		updater.dispatcher.add_handler(document_message_handler)
		updater.dispatcher.add_handler(audio_handler)

		updater.start_polling()
		updater.idle()
   
