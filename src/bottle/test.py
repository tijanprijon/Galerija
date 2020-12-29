import bottle   # TODO pip install not working, currently entire bottle.py file copied to rep
from bottle import get, post, request

bottle.TEMPLATE_PATH.insert(0,'C:\\Users\\Uporabnik\\Tijan\\projekt_rac\\Galerija\\src\\bottle\\view')    # TODO add to gitignore config file or change to relative path

@bottle.get('/')
def hello():
    if request.get_cookie('account'):
        # user = request.get_cookie('account')
        return bottle.template("test12.tpl")
    bottle.redirect('/login')

@get('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
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


@post('/login')
def do_login():
    username = request.forms.get("username")
    password = request.forms.get("password")
    if check_login(username, password):
        bottle.response.set_cookie("account", username)
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>ane<p>"


bottle.run(host='localhost', port=8080, debug=True, reloader = True)