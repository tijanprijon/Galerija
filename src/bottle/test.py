import bottle   # TODO pip install not working, currently entire bottle.py file copied to rep

bottle.TEMPLATE_PATH.insert(0,'C:\\Users\\Uporabnik\\Tijan\\New folder\\Galerija\\bottle\\view')    # TODO add to gitignore config file or change to relative path
@bottle.get('/')
def hello():
    #return bottle.template("test12.tpl")
    if bottle.request.get_cookie("user"):
        return "Welcome back! Nice to see you again"
    else:
        bottle.response.set_cookie("user", "yes")
        return "Hello there! Nice to meet you"

bottle.run(host='localhost', port=8080, debug=True, reloader = True)