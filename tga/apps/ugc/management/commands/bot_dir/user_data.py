class User_params():    
     def __init__(self):
        self.chat_id = None
        self.select_language = False
        self.language = None


        self.data = ''
        self.email = None

        self.add_channel = False
        self.remove_channel = False

        self.date = None
        
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
        
        self.language_change = False
        self.check_email = False
        self.help = False


class Users():
    def __init__(self):
        self.user = {}    