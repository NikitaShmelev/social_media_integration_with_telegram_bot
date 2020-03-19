from telegram import KeyboardButton, ReplyKeyboardMarkup
from .translates import translates


LANGUAGE_RU = 'Русский'
LANGUAGE_EN  = 'English'


def start_keyboard(user):
    keyboard = [
        [
            KeyboardButton(translates[user.language]['BUTTON3_BOT_HELP']),
        ],
        [
            KeyboardButton(translates[user.language]['BUTTON4_CREATE_POST']),
            KeyboardButton(translates[user.language]['show_posts']),
        ],
        [   
            KeyboardButton(translates[user.language]['list_of_channels']),
            KeyboardButton(translates[user.language]['add_channel']),
            KeyboardButton(translates[user.language]['remove_channel'])
        ],
        [
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
    keyboard = [
        [
            KeyboardButton(translates[user.language]['START_PAGE']),
        ],
    ]
    if len(user.unpublished_posts) > 0:
        for i in user.unpublished_posts.keys():
            keyboard.append(
                [
                KeyboardButton(
                    user.unpublished_posts[i]
                    ),
                ]
                )
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        )


def post_keyboard(user):
    if user.unpublished_keyboard:
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
        if user.location[0]:
            keyboard[1][1] = KeyboardButton(translates[user.language]['DELETE_LOCATION'])
        elif user.text[1] != '':
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
    if user.location[1]:
        keyboard[1][1] = KeyboardButton(
            translates[user.language]['DELETE_LOCATION'])
    if user.text[1] != '':
        keyboard[1][0] = KeyboardButton(
            translates[user.language]['DELETE_TEXT'])
    # if user.media[1] != '':
    #     keyboard[1].append(KeyboardButton(translates[user.language]['DELETE_MEDIA']))
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def email_keyboard(user):
    keyboard = [
        [
            KeyboardButton(translates[user.language]['tap email again']),
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
    for i in user.channels:
        keyboard.append([KeyboardButton(str(i))])
    if user.all_channels:
        keyboard.append([KeyboardButton(translates[user.language]['ALL_CHANNELS'])])
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        )
