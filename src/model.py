from datetime import datetime
from PIL import Image, ImageFilter
import os
import json

path_to_json = os.path.join("Galerija", "database", "data.json")
picture_path = os.path.join("Galerija", "database")

def read_json():
    with open(path_to_json, "r") as json_file:
        data = json.load(json_file)
        return data

def write_json(data):
    with  open(path_to_json, "w") as outfile:
        json.dump(data, outfile, indent=4)

# USERS MANEGING

def check_login(username, password):
    """Return True if login infos are valid"""
    data = read_json()
    for user in data["users"]:
        if user["Username"] == username and user["Password"] == password:
            return True
    return False

def username_available(name):
    """return True if available, otherwise False"""
    data = read_json()
    for user in data["users"]:
        if user["Username"] == name:
            return False
    return True

def add_account(username, password):
    data = read_json()
    data_to_add = {"Username": username, "Password" : password}
    data["users"].append(data_to_add)
    write_json(data)

def get_list_of_images(user):
    list_of_images = list()
    data = read_json()
    for element in data:
        if type(data[element]) == list: # element in json is not picture but list of users
            continue
        if data[element]["owner"] == user:
            list_of_images.append(data[element])
    return list_of_images



# PICTURES MANEGING

def save_picture(user, upload):
    name, ext = os.path.splitext(upload.filename)
    save_path =  os.path.join(picture_path, f"{name}_{user}{ext}")
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'
    with open(save_path, "wb") as image_file:
        image_file.write(upload.file.read())
    data = read_json()
    try:
        data[f"{name}_{user}"]
        print("Picture already exists.")
        return None
    except Exception:
        pass
    data[f"{name}_{user}"] = {"owner": user, "likes" : 0, "image_name": f"{name}_{user}", "dislikes" : 0, "comments" : [], "date": datetime.now().__str__(), "ext": ext}
    write_json(data)

def save_grayscale(image_name, ext, user):
    image_path = os.path.join(picture_path, f"{image_name}{ext}")
    original_image = Image.open(image_path)
    gray_scale_image = original_image.convert('1')
    save_path =  os.path.join(picture_path, f"{image_name}_grayscale{ext}")
    gray_scale_image.save(save_path)
    data = read_json()
    data[f"{image_name}_grayscale"] = {"owner": user, "likes" : 0, "image_name": f"{image_name}_grayscale", "dislikes" : 0, "comments" : [], "date": datetime.now().__str__(), "ext": ext}
    write_json(data)

def save_diff_filters(image_name, ext, filter_name, user):
    """Possible names: BLUR, EMBOSS, EDGE_ENHANCE, EDGE_ENHANCE_MORE, CONTOUR."""
    image_path = os.path.join(picture_path, f"{image_name}{ext}")
    original_image = Image.open(image_path)
    filtered_image = original_image.filter(getattr(ImageFilter, filter_name))
    save_path =  os.path.join(picture_path, f"{image_name}_{filter_name}{ext}")
    filtered_image.save(save_path)
    data = read_json()
    data[f"{image_name}_{filter_name}"] = {"owner": user, "likes" : 0, "image_name": f"{image_name}_{filter_name}", "dislikes" : 0, "comments" : [], "date": datetime.now().__str__(), "ext": ext}
    write_json(data)

def like_picture(image_name):
    data = read_json()
    data[image_name]["likes"] += 1
    write_json(data)

def dislike_picture(image_name):
    data = read_json()
    data[image_name]["dislikes"] += 1
    write_json(data)

def add_comment(image_name, comment):
    data = read_json()
    data[image_name]["comments"].append(comment)
    write_json(data)