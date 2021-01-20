from datetime import datetime
from PIL import Image, ImageFilter
import os
import json
import re
path_to_json = os.path.join(os.getcwd(),'..', "database", "data.json")
picture_path = os.path.join(os.getcwd(),'..', "database")

def read_json():
    with open(path_to_json, "r") as json_file:
        data = json.load(json_file)
        return data

def write_json(data):
    with  open(path_to_json, "w") as outfile:
        json.dump(data, outfile, indent=4)

# USERS MANEGING

def check_grammar(word):
    if re.match("^[A-Za-z0-9_-]*$", word):
        return True
    return False

def check_login(username, password):
    """Return True if login infos are valid"""
    if check_grammar(username) and check_grammar(password):
        data = read_json()
        for user in data["users"]:
            if user["username"] == username and user["password"] == password:
                return True
    return False

def username_available(name, password):
    """return True if available, otherwise False"""
    if not( check_grammar(name) and check_grammar(password)):
        return False
    data = read_json()
    for user in data["users"]:
        if user["username"] == name:
            return False
    return True

def add_account(username, password):
    data = read_json()
    data_to_add = {"username": username, "password" : password, "sort_preference" : [None, True], "show_pictures" : "show_all"}
    data["users"].append(data_to_add)
    write_json(data)

def get_list_of_images(user):    # Possible sorting options: likes, dislikes, date, comments (number of)
    data = read_json()
    for element in data["users"]:
        if element["username"] == user:
            show_only = element["show_pictures"]
            order_by, in_reverse = element["sort_preference"]
            if in_reverse == "reverse":
                in_reverse = True
            else:
                in_reverse = False
    
    def sort_by(elem):
        if order_by == "comments":
            return len(elem["comments"])
        else:
            return elem[order_by]

    list_of_images = list()
    for element in data:
        if type(data[element]) == list: # element in json is not picture but list of users
            continue
        if data[element]["owner"] == user and (show_only in data[element]["labels"] or show_only == "show_all"):
            list_of_images.append(data[element])
    if order_by:
        list_of_images.sort(key = sort_by, reverse = in_reverse)
    return list_of_images

def add_user_sort_preference(user, order_by, in_reverse):
    data = read_json()
    for element in data["users"]:
        if element["username"] == user:
            element["sort_preference"] = [order_by, in_reverse]
    write_json(data)

def user_set_view(user, label):
    data = read_json()
    for element in data["users"]:
        if element["username"] == user:
            element["show_pictures"] = label
    write_json(data)

# PICTURES MANEGING
def resize_picture(image_path, basewidth):
    img = Image.open(image_path)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(image_path)

def save_picture(user, upload):
    name, ext = os.path.splitext(upload.filename)
    save_path =  os.path.join(picture_path, f"{name}_{user}{ext}")
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'
    with open(save_path, "wb") as image_file:
        image_file.write(upload.file.read())
    resize_picture(save_path, 800)
    data = read_json()
    if data.get(f"{name}_{user}", None):    # If picture already exists dont save it.
        return None
    data[f"{name}_{user}"] = {"owner": user, "likes" : 0, "image_name": f"{name}_{user}", "dislikes" : 0, "comments" : [], "date": datetime.now().__str__(), "ext": ext, "labels" : []}
    write_json(data)

def save_grayscale(image_name, ext, user):
    image_path = os.path.join(picture_path, f"{image_name}{ext}")
    original_image = Image.open(image_path)
    gray_scale_image = original_image.convert('1')
    save_path =  os.path.join(picture_path, f"{image_name}_grayscale{ext}")
    gray_scale_image.save(save_path)
    resize_picture(save_path, 800)
    data = read_json()
    data[f"{image_name}_grayscale"] = {"owner": user, "likes" : 0, "image_name": f"{image_name}_grayscale", "dislikes" : 0, "comments" : [], "date": datetime.now().__str__(), "ext": ext, "labels" : ["filter"]}
    write_json(data)

def save_diff_filters(image_name, ext, filter_name, user):
    """Possible names: BLUR, EMBOSS, EDGE_ENHANCE, EDGE_ENHANCE_MORE, CONTOUR."""
    image_path = os.path.join(picture_path, f"{image_name}{ext}")
    original_image = Image.open(image_path)
    filtered_image = original_image.filter(getattr(ImageFilter, filter_name))
    save_path =  os.path.join(picture_path, f"{image_name}_{filter_name}{ext}")
    filtered_image.save(save_path)
    data = read_json()
    data[f"{image_name}_{filter_name}"] = {"owner": user, "likes" : 0, "image_name": f"{image_name}_{filter_name}", "dislikes" : 0, "comments" : [], "date": datetime.now().__str__(), "ext": ext, "labels" : ["filter"]}
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

def add_label(image_name, label):
    data = read_json()
    data[image_name]["labels"].append(label)
    write_json(data)

def remove_label(image_name, label):
    data = read_json()
    data[image_name]["labels"].remove(label)
    write_json(data)