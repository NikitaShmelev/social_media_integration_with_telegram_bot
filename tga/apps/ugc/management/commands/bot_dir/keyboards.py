from telegram import KeyboardButton, ReplyKeyboardMarkup
from .translates import translates


LANGUAGE_RU = 'Русский'
LANGUAGE_EN  = 'English'



def start_page_keyboard(user):
    keyboard = [
        [
            KeyboardButton(translates[user.language]['START_PAGE']),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
    

def help_keyboard(user):
    keyboard = [
        [
            KeyboardButton(translates[user.language]['START_PAGE']),
        ],
        [
            KeyboardButton(translates[user.language]['how_to_create']),
            KeyboardButton(translates[user.language]['how_to_update']),
            KeyboardButton(translates[user.language]['work_with_channels']),
        ],
        [
            KeyboardButton(translates[user.language]['location_guide']),
            KeyboardButton(translates[user.language]['media_guide']),
            KeyboardButton(translates[user.language]['text_guide']),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def start_keyboard(user):
    keyboard = [
        [
            KeyboardButton(translates[user.language]['view_current_post']) if user.event[0] else KeyboardButton(translates[user.language]['BUTTON4_CREATE_POST']),
            
        ],
        [
            KeyboardButton(translates[user.language]['show_posts'])
        ],
        [   
            KeyboardButton(translates[user.language]['list_of_channels']),
            KeyboardButton(translates[user.language]['add_channel']),
            KeyboardButton(translates[user.language]['remove_channel'])
        ],
        [   

            KeyboardButton(translates[user.language]['BUTTON3_BOT_HELP']),
            KeyboardButton(translates[user.language]['CHANGE_LANGUAGE']),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        )


def conifrm_keyboard(user):
    keyboard = [
        [
            KeyboardButton(translates[user.language]['START_PAGE']),
        ],
        [
            KeyboardButton(translates[user.language]['CONFIRM_YES']),
            KeyboardButton(translates[user.language]['CONFIRM_NO']),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        )


def unpublished_keyboard(user):
    keyboard = list()
    if len(user.unpublished_posts) > 0:
        for i in user.unpublished_posts.keys():
            keyboard.append(
                [
                KeyboardButton(
                    str(user.unpublished_posts[i].created_at)
                    ),
                ]
                )
        keyboard.reverse()
        keyboard.insert(0, [
            KeyboardButton(translates[user.language]['START_PAGE']),
        ],)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        )


def post_keyboard(user):
    if user.unpublished_keyboard or user.update_post:
        return find_post_keyboard(user)
    else:
        keyboard = [
            [
                KeyboardButton(translates[user.language]['START_PAGE']),
            ],
            [
                KeyboardButton(translates[user.language]['BUTTON5_TEXT_FOR_POST']),
                KeyboardButton(translates[user.language]['BUTTON6_ADD_LOCATION']),
                KeyboardButton(translates[user.language]['BUTTON7_ADD_MEDIA']),
            ],
            [
                KeyboardButton(translates[user.language]['BUTTON10_CANCEL_POST']),
                KeyboardButton(translates[user.language]['BUTTON9_SAVE_POST']),
                KeyboardButton(translates[user.language]['BUTTON8_SHOW_POST']),
            ],
            [
                KeyboardButton(translates[user.language]['publish_and_save']),
            ],
        ]
        if user.post.location[1]:
            keyboard[1][1] = KeyboardButton(translates[user.language]['DELETE_LOCATION'])
        if user.post.text[1] != '':
            keyboard[1][0] = KeyboardButton(translates[user.language]['DELETE_TEXT'])
        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            )


def find_post_keyboard(user):
    keyboard = [
        [
            KeyboardButton(translates[user.language]['START_PAGE']),
        ],
        [
            KeyboardButton(translates[user.language]['BUTTON5_TEXT_FOR_POST']),
            KeyboardButton(translates[user.language]['BUTTON6_ADD_LOCATION']),
            KeyboardButton(translates[user.language]['BUTTON7_ADD_MEDIA']),
        ],
        [
            KeyboardButton(translates[user.language]['BUTTON10_CANCEL_POST']),
            KeyboardButton(translates[user.language]['update_post']),
            KeyboardButton(translates[user.language]['BUTTON8_SHOW_POST']),
        ],
        [
            KeyboardButton(translates[user.language]['publish_and_update']),
        ],
    ]
    if user.post.location[1]:
        keyboard[1][1] = KeyboardButton(
            translates[user.language]['DELETE_LOCATION'])
    if user.post.text[1] != '':
        keyboard[1][0] = KeyboardButton(
            translates[user.language]['DELETE_TEXT'])
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def email_keyboard(user):
    keyboard = [
        [
            KeyboardButton(translates[user.language]['send_email_again']),
        ],
        [
            KeyboardButton(translates[user.language]['BUTTON_SEND_CODE']),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        )

def regisration_keyboard(user):
    keyboard = [
        [   
            KeyboardButton(translates[user.language]['REGISTER_ME']),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        )


def language_keyboard(user):
    keyboard = [
        [
            KeyboardButton(LANGUAGE_RU),
            KeyboardButton(LANGUAGE_EN),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        )


def channels_keyboard(user):
    keyboard = [
        [
            KeyboardButton(translates[user.language]['START_PAGE']),
        ],
    ]
    for i in user.channels[1:]:
        keyboard.append([KeyboardButton(str(i))])
        # or user.save_and_publish or user.update_and_publish
    if user.channels[0] or (len(user.channels) > 1 and (user.save_and_publish or user.update_and_publish)):
        keyboard.append([KeyboardButton(translates[user.language]['ALL_CHANNELS'])])
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
