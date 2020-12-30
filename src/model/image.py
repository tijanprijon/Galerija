from datetime import datetime
from PIL import Image, ImageFilter

path = "C:\\Users\\Uporabnik\\Tijan\\projekt_rac\\Galerija\\src\\model\\pictures"   # TODO relative path
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

    def add_colorles_filter(self):
        original_image = Image.open(f"{path}\\{self.image_name}.png")
        gray_scale_image = original_image.convert('1')
        gray_scale_image.save(f"{path}\\{self.image_name}_grayscale.png")
        return Images(f"{self.image_name}_colorles", datetime.now())

    def add_dif_filter(self, filter_name):
        """Possible names: BLUR, EMBOSS, EDGE_ENHANCE, EDGE_ENHANCE_MORE, CONTOUR.""" 
        original_image = Image.open(f"{path}\\{self.image_name}.png")
        filtered_image = original_image.filter(getattr(ImageFilter, filter_name))
        filtered_image.save(f"{path}\\{self.image_name}_{filter_name}.png")
        return Images(f"{self.image_name}_{filter_name}", datetime.now())