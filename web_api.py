import os
import hashlib
from flask import Flask
from flask import redirect
from flask import request
app = Flask(__name__)
some_data = {
    "usernames":{
        "w0nzy":{
            "has_logged_in":False,
            "password":"w0nzy",
            "session_id":None
        }
    }
}
html = "<head>\n<title>Wrong</title>\n</head>\n<body>"
@app.route("/Login")
def login_this():
    global some_data
    username = request.args.get("userName")
    password = request.args.get("passWord")
    global session_id
    session_id = hashlib.sha224(os.urandom(400)).hexdigest()
    if not some_data["usernames"].get(username):
        return html+"\n<h1>Invalid username %s username is not exists" % (username)+ "\n"+"</body>"
    else:
        if password != some_data["usernames"][username].get("password"):
            return html+"\n"+"Incorrect password of %s" % (username) + "\n"+"</body>"
        else:
            usersession = some_data["usernames"][username]["session_id"]
            some_data["usernames"][username]["session_id"]=session_id
            some_data["usernames"][username]["has_logged_in"]=True
            logged_in_data = some_data["usernames"][username]["has_logged_in"]
            if not logged_in_data:
                return redirect("http://192.168.1.124:8000/Panel?userName=%s&sessionID=%s" % (username,session_id),code=302)
            else:
                return html+"<h1>You are already logged in </h1>"+"</body>"
@app.route("/Panel")
def _redirected():
    global some_data
    username = request.args.get("userName")
    session_username = request.args.get("sessionID")
    if not some_data["usernames"].get(username) is None:
        session_id = some_data["usernames"][username].get("session_id")
        password = some_data["usernames"][username].get("password")
        if session_id == session_username:
            return html+"<ul type='circle'>\n<li>> You have been logged in your Username: %s \n<li>Your password: %s </li>\n<li>Your session id is: %s </li>\n</ul></body>" % (username,password,session_id)
            some_data["usernames"][username]["session_id"]=None
            some_data["usernames"][username]["has_logged_in"]=False
        else:
            return html+"<h1>You are not logged in</h1></body>"
    some_data["usernames"][username]["session_id"]=None
    some_data["usernames"][username]["has_logged_in"]=False
@app.route("/CreateNewUser")
def create_user():
    global some_data
    new_user_id = request.args.get("username")
    pass_ = request.args.get("password")
    if pass_ is None:
        return html+"<h1> Password must be filled</h1>\n</nbody>"
    elif new_user_id is None:
        return html+"<h1> Username must be filled</h1>\n</nbody>"
    else:
        try:
            some_data["usernames"][new_user_id]={"password":pass_,"session_id":None,"has_logged_in":False}
            return html+"<h1>Succes and now login with your credentials</h1>"+"</body>"
        except:
            return html+"\n<h1>Rahatsizlik verdigimiz icin ozur dileriz yetkili birimlerimize ilettik en kisa surede halledecegiz"+"\n"+"</body>"
app.run("192.168.1.124",8000)