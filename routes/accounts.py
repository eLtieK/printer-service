from flask import Blueprint, abort, request, session, redirect
from flask_cors import CORS
import requests
from controllers import accounts_controller
from config import google_auth
import cachecontrol
import google
from google.oauth2 import id_token

account_route = Blueprint('account_route', __name__)
CORS(account_route, supports_credentials=True, origins=["http://localhost:3000"]) #link toi fe

@account_route.route('/account/login')
def login():
    authorization_url, state = google_auth.flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@account_route.route('/account/callback')
def callback():
    google_auth.flow.fetch_token(authorization_response=request.url)
    
    if not session["state"] == request.args["state"]:
        abort(500) 

    credentials = google_auth.flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=google_auth.GOOGLE_CLIENT_ID
    )
    
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/account/protected_area")

@account_route.route('/account/logout')
def logout():
    session.clear()
    return redirect("/account/")

@account_route.route('/account/')
def index():
    return "Hello world! <a href='/account/login'> <button>Login</button> </a>" 

@account_route.route('/account/protected_area')
@accounts_controller.login_is_required
def protected_area():
    return "Protected! <a href='/account/logout'> <button>Logout</button> </a>"