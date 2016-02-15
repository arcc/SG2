# This file is for user class
class USER(object):
    """This is a class for sg2 user
    """
    def __init__(self, username, **kwargs):
        self.name = username
        self.email = None
        self.privilege_level = None
        self.num_images_processed = 0
        self.accurate_rate = 0.0
