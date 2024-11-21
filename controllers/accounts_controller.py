#logic
from flask import session, abort

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401) #Authorization required
        else: 
            return function()
        
    return wrapper