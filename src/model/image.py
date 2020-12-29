from datetime import datetime

class Images:

    def __init__(self, image_name, oldness):
        self.image_name = image_name
        self.oldness = oldness
        self.comment = list()
        self.likes = 0
        self.dislikes = 0

    def like_picture(self):
        self.likes += 1
    
    def dislike_picture(self):
        self.dislikes += 1

    def comment_picture(self, text):
        self.comment.append(text)

    def add_blur_filter(self):
        # TODO
        return Images(f"{self.image_name}_blured", datetime.now())

    def add_colorles_filter(self):
        # TODO
        return Images(f"{self.image_name}_colorles", datetime.now())