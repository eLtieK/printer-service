#logic
from flask import session, abort
from models import data

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401) #Authorization required
        elif session.get("role") == "guest": 
            state_value = session.get("state") 
            session.clear() # Clear all session data 
            session["state"] = state_value
            return "Please provide an appropriate account to access this area <a href='/account'> <button>Return</button> </a>"
        else: 
            return function()
        
    return wrapper

def get_user_role(email):
    return data.user_roles.get(email, "guest")

