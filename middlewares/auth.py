from flask import abort, request, session

def login_is_required(function):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return abort(401) #Authorization required
        elif session.get("role") == "guest": 
            state_value = session.get("state") 
            session.clear() # Clear all session data 
            session["state"] = state_value
            return "Please provide an appropriate account to access this area <a href='/account'> <button>Return</button> </a>"
        else: 
            return function(*args, **kwargs)
    wrapper.__name__ = function.__name__ + "_login"
    return wrapper

def spso_is_required(function):
    def wrapper(*args, **kwargs):
        role = request.headers.get('Role')
        if not role or role != "Spso":
            return abort(403)  # Authorization required
        else: 
            return function(*args, **kwargs)
    wrapper.__name__ = function.__name__ + "_spso"
    return wrapper

def student_is_required(function):
    def wrapper(*args, **kwargs):
        role = request.headers.get('Role')
        if not role or role != "Student":
            return abort(403)  # Authorization required
        else: 
            return function(*args, **kwargs)
    wrapper.__name__ = function.__name__ + "_student"
    return wrapper