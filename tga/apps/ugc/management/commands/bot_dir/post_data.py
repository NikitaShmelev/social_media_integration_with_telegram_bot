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
        self.unpublished_keyboard = False
        self.show_unpublished_posts = False
        self.all_channels = False