import bottle   # TODO pip install not working, currently entire bottle.py file copied to rep
import os
import json
from bottle import get, post, request
from datetime import datetime
from PIL import Image, ImageFilter
from pathlib import Path

bottle.TEMPLATE_PATH.insert(0,'Galerija\\src\\bottle\\view')    # TODO add to gitignore config file or change to relative path
path_to_json = 'Galerija\\src\\model\\'
picture_path = "Galerija\\static\\images\\"
#path_to_pictures = "C:\\Users\\Uporabnik\\Tijan\\projekt_rac\\Galerija\\static\\"

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


app = bottle.default_app()
bottle.BaseTemplate.defaults['get_url'] = app.get_url

@bottle.route('/static/<filename:path>', name='static')
def serve_static(filename):
    return bottle.static_file(filename, root= "Galerija\\static")

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

@get('/')
def main_page():
    if request.get_cookie('account'):
        user = request.get_cookie('account')
    else:
        user = "Guest"
    return bottle.template("main_page.tpl", name = user)

@post('/')
def main_page_action():
    if request.forms.get("login"):
        bottle.redirect('/login')
    if request.forms.get("gallery"):
        bottle.redirect('/gallery')

@get('/login')
def login():
    if request.get_cookie('account'):
        return "You are already logged in :)"
    return bottle.template("login.tpl", name = request.get_cookie('account'))

@post('/login')
def do_login():

    #login
    if request.forms.get("username") and request.forms.get("password"): # not None
        username = request.forms.get("username")
        password = request.forms.get("password")
        if check_login(username, password):
            bottle.response.set_cookie("account", username)
            print("Your login information was correct.")
            bottle.redirect('/')
        else:
            return("Your username or password is incorrect.")
        return "<p>HA HA HA<p>" #login unsuccessful

    #sign in
    elif request.forms.get("new_username") and request.forms.get("new_password"):   # not None
        new_username = request.forms.get("new_username")
        password = request.forms.get("new_password")
        if username_available(new_username):
            bottle.response.set_cookie("account", new_username)
            add_account(new_username, password)
            bottle.redirect('/')
            print("Sign in successful")
        else:
            return f"Username '{new_username}' already exists."
    else:
        return "<p>HA HA HA. Not working<p>" #login unsuccessful


@get('/gallery')
def gallery():
    if request.get_cookie('account'):
        user = request.get_cookie('account')
        images = get_list_of_images(user)
        return bottle.template("gallery.tpl", images = images)
    return bottle.redirect("/login")

@post('/gallery')
def gallery_action(): # TODO call functions
    if not request.get_cookie('account'):
        bottle.redirect('/')
    user = request.get_cookie('account')
    if request.files.get('upload'):
        upload = request.files.get('upload')
        save_picture(user, upload)
        bottle.redirect('/gallery')
    if request.forms.get("main_page"):
        bottle.redirect("/")
    for image in get_list_of_images(user):
        like_name = f"like_{image['image_name']}"
        dislike_name = f"dislike_{image['image_name']}"
        comment_name = f"comment_{image['image_name']}"
        filter_name = f"filter_{image['image_name']}"
        if request.forms.get(like_name):
            like_picture(f"{image['image_name']}")
            bottle.redirect('/gallery')
        if request.forms.get(dislike_name):
            dislike_picture(f"{image['image_name']}")
            bottle.redirect('/gallery')
        if request.forms.get(comment_name):
            add_comment(f"{image['image_name']}", request.forms.get(comment_name))
            bottle.redirect('/gallery')
        if request.forms.get(filter_name):
            if request.forms.get(filter_name) == "GRAYSCALE":
                save_grayscale(image['image_name'], image['ext'], user)
                bottle.redirect('/gallery')
            else:
                save_diff_filters(image['image_name'], image['ext'], request.forms.get(filter_name), user)
                bottle.redirect('/gallery')

bottle.run(host='localhost', port=8080, debug=True, reloader = True)
