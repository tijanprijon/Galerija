import bottle   # TODO pip install not working, currently entire bottle.py file copied to rep
import os
import sys
from bottle import get, post, request
from datetime import datetime
from model import *

bottle.TEMPLATE_PATH.insert(0,os.path.join("Galerija", "src", "view"))    # TODO add to gitignore config file or change to relative path

app = bottle.default_app()
bottle.BaseTemplate.defaults['get_url'] = app.get_url

@bottle.route('/database/<filename:path>', name='database')
def serve_static(filename):
    return bottle.static_file(filename, root= os.path.join("Galerija", "database"))

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
