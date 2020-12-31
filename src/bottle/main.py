import bottle   # TODO pip install not working, currently entire bottle.py file copied to rep
import os
import json
from bottle import get, post, request
from datetime import datetime


bottle.TEMPLATE_PATH.insert(0,'C:\\Users\\Uporabnik\\Tijan\\projekt_rac\\Galerija\\src\\bottle\\view')    # TODO add to gitignore config file or change to relative path
path_to_json = 'C:\\Users\\Uporabnik\\Tijan\\projekt_rac\\Galerija\\src\\model\\'
path_to_pictures = "C:\\Users\\Uporabnik\\Tijan\\projekt_rac\\Galerija\\src\\model\\pictures\\"

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
    save_path =  f"C:\\Users\\Uporabnik\\Tijan\\projekt_rac\\Galerija\\src\\model\\pictures\\{name}_{user}{ext}"
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
    data[f"{name}_{user}"] = {"owner": user, "likes" : 0, "dislikes" : 0, "comments" : [], "date": datetime.now().__str__()}
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

def add_account(username, password):
    with open(f"{path_to_json}data.txt", "r") as json_file:
        data = json.load(json_file)
    data_to_add = {"Username": username, "Password" : password}
    data["users"].append(data_to_add)
    with open(f"{path_to_json}data.txt", "w") as outfile:
        json.dump(data, outfile, indent=4)

def like_picture():
    pass

def dislike_picture():
    pass

def add_comment():
    pass

def upload_filtered_picture():
    pass

def upload_blured_picture():
    pass

@get('/')
def main_page():
    if request.get_cookie('account'):
        user = request.get_cookie('account')
    else:
        user = "Guest"
    return bottle.template("test12.tpl", name = user)

@post('/')
def main_page_action():
    if request.forms.get("login"):
        bottle.redirect('/login')
    if request.forms.get("galary"):
        bottle.redirect('/galery')
    if request.forms.get("upload"):
        bottle.redirect('/upload')

@get('/upload')
def upload_pictures():
    if request.get_cookie('account'):
        return bottle.template("upload.tpl", name = request.get_cookie('account'))
    bottle.redirect('/login')

@post('/upload')
def upload_pictures():
    user = request.get_cookie('account')
    upload = request.files.get('upload')
    save_picture(user, upload)
    return 'Successful:)'

@get('/login')
def login():
    if request.get_cookie('account'):
        return "You are already logged in:o"
    return '''
        <b>Already have an account? Login</b> :
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>

        <b>First time? Sign in:</b>

        <form action="/login" method="post">
            New username: <input name="new_username" type="text" />
            New password: <input name="new_password" type="password" />
            <input value="Sign in" type="submit" />
        </form>
    '''

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


@get('/galery')
def galery():
    if request.get_cookie('account'):
        user = request.get_cookie('account')
        images = get_list_of_images(user)
        return bottle.template("view_pictures.tpl", images = images, path = path_to_pictures)
    return "://"
# @post('/galery')
# def galery():
#     if request.get_cookie('account'):
#         return bottle.template("view_pictures.tpl")
bottle.run(host='localhost', port=8080, debug=True, reloader = True)