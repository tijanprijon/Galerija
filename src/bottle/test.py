import bottle   # TODO pip install not working, currently entire bottle.py file copied to rep
from bottle import get, post, request

bottle.TEMPLATE_PATH.insert(0,'C:\\Users\\Uporabnik\\Tijan\\projekt_rac\\Galerija\\src\\bottle\\view')    # TODO add to gitignore config file or change to relative path

@bottle.get('/')
def hello():
    if request.get_cookie('account'):
        user = request.get_cookie('account')
        return bottle.template("test12.tpl", name = user)
    bottle.redirect('/login')

@get('/login')
def login():
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

def check_login(username, password):
    if username == "Tijan" and password == "Prijon":
        return True
    usernames = ["Tijan", "Miha"]   # test
    passwords = ["Prijon", "Tijan", "Miha", "legenda123"]
    if username in usernames and password in passwords:
        return True
    else:
        return False

def check_username(username):
    if username == "Tijan":
        return False
    return True

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
        return "<p>HA HA HA<p>" #login unsuccessful

    #sign in
    elif request.forms.get("new_username") and request.forms.get("new_password"):
        new_username = request.forms.get("new_username")
        password = request.forms.get("new_password")
        if check_username(new_username):  # not None
            bottle.response.set_cookie("account", new_username)
            print("Sign in successful")
            bottle.redirect('/')
            
    else:
        return "<p>HA HA HA<p>" #login unsuccessful


bottle.run(host='localhost', port=8080, debug=True, reloader = True)