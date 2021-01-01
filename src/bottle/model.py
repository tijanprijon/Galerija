from datetime import datetime
from PIL import Image, ImageFilter
import os
import json


path_to_json = 'Galerija\\src\\model\\'
picture_path = "Galerija\\static\\images\\"

def check_login(username, password):
    """Return True if login infos are valid"""
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
    for user in data["users"]:
        if user["Username"] == username and user["Password"] == password:
            return True
    return False

def username_available(name):
    """return True if available, otherwise False"""
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
    for user in data["users"]:
        if user["Username"] == name:
            return False
    return True

def save_picture(user, upload): #TODO title
    name, ext = os.path.splitext(upload.filename)
    save_path =  f"{picture_path}{name}_{user}{ext}"
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'
    with open(save_path, "wb") as image_file:
        image_file.write(upload.file.read())
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
        try:
            data[f"{name}_{user}"]
            print("Picture already exists")
            return None
        except Exception:
            pass
    data[f"{name}_{user}"] = {"owner": user, "likes" : 0, "image_name": f"{name}_{user}", "dislikes" : 0, "comments" : [], "date": datetime.now().__str__(), "ext": ext}
    with open(f"{path_to_json}data.txt", "w") as outfile:
        json.dump(data, outfile, indent=4)

def get_list_of_images(user):
    list_of_images = list()
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
    for element in data:
        if type(data[element]) == list: # element in json is not picture but list of users
            continue
        if data[element]["owner"] == user:
            list_of_images.append(data[element])
    return list_of_images

def save_grayscale(image_name, ext,  user):
    original_image = Image.open(f"{picture_path}{image_name}{ext}")
    gray_scale_image = original_image.convert('1')
    gray_scale_image.save(f"{picture_path}{image_name}_grayscale{ext}")
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
    data[f"{image_name}_grayscale"] = {"owner": user, "likes" : 0, "image_name": f"{image_name}_grayscale", "dislikes" : 0, "comments" : [], "date": datetime.now().__str__(), "ext": ext}
    with open(f"{path_to_json}data.txt", "w") as outfile:
        json.dump(data, outfile, indent=4)

def save_diff_filters(image_name, ext, filter_name,  user):
    """Possible names: BLUR, EMBOSS, EDGE_ENHANCE, EDGE_ENHANCE_MORE, CONTOUR.""" 
    original_image = Image.open(f"{picture_path}{image_name}{ext}")
    filtered_image = original_image.filter(getattr(ImageFilter, filter_name))
    filtered_image.save(f"{picture_path}{image_name}_{filter_name}{ext}")
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
    data[f"{image_name}_{filter_name}"] = {"owner": user, "likes" : 0, "image_name": f"{image_name}_{filter_name}", "dislikes" : 0, "comments" : [], "date": datetime.now().__str__(), "ext": ext}
    with open(f"{path_to_json}data.txt", "w") as outfile:
        json.dump(data, outfile, indent=4)

def add_account(username, password):
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
    data_to_add = {"Username": username, "Password" : password}
    data["users"].append(data_to_add)
    with open(f"{path_to_json}data.txt", "w") as outfile:
        json.dump(data, outfile, indent=4)

def like_picture(image_name):
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
    data[image_name]["likes"] += 1
    with open(f"{path_to_json}data.txt", "w") as outfile:
        json.dump(data, outfile, indent=4)

def dislike_picture(image_name):
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
    data[image_name]["dislikes"] += 1
    with open(f"{path_to_json}data.txt", "w") as outfile:
        json.dump(data, outfile, indent=4)

def add_comment(image_name, comment):
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
    data[image_name]["comments"].append(comment)
    with open(f"{path_to_json}data.txt", "w") as outfile:
        json.dump(data, outfile, indent=4)