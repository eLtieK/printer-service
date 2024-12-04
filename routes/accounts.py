from flask import Blueprint, abort, jsonify, render_template, request, session, redirect
from flask_cors import CORS
import requests
from controllers import accounts_controller
from middlewares.auth import login_is_required
from config import google_auth
import cachecontrol
import google
from google.oauth2 import id_token

account_tuple = (Blueprint('account_route', __name__), '/account')
account_route, prefix_route = account_tuple
CORS(account_route, supports_credentials=True, origins=["http://localhost:3000"]) #link toi fe

@account_route.route('/modify_data', methods=['PUT'])
def modify_data():
    data = request.get_json() 
    email = data.get('email') 
    name = data.get('name')
    phone = data.get('phone')

    return accounts_controller.create_or_alter_account(email, name, phone)

@account_route.route('/create', methods=['POST'])
def create():
    data = request.get_json() 
    email = data.get('email') 
    role = data.get('role')

    return accounts_controller.create_account(email, role)

@account_route.route('/get', methods=['GET'])
def get():
    return accounts_controller.get_all_accounts()

@account_route.route('/login')
def login():
    session.clear()
    authorization_url, state = google_auth.flow.authorization_url() #url uỷ quyền cho OAuth2 của google
    session["state"] = state
    return redirect(authorization_url) #chuyển đến trang uỷ quyền

@account_route.route('/callback')
def callback():
    google_auth.flow.fetch_token(authorization_response=request.url) #lấy token OAuth2
    
    # if "state" not in session or not session["state"] == request.args["state"]: #xác thực tham số state
    #     abort(500) 

    #Xác thực và giải mã ID token để lấy thông tin người dùng
    credentials = google_auth.flow.credentials
    access_token = credentials.token

    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=google_auth.GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=60 # Allow for up to 60 seconds of clock skew
    )
    
    #Lưu thông tin người dùng vào session
    email = id_info.get("email")
    role = accounts_controller.get_account_role(email)

    # Trả về token và thông tin người dùng dưới dạng JSON
    frontend_url = ''
    if(role == 'spso') :
        frontend_url = "http://localhost:3000/spso"
    elif(role == 'student') :
        frontend_url = "http://localhost:3000/student"
    elif(role == 'admin') :
        frontend_url = "http://localhost:3000/admin"

    return redirect(f"{frontend_url}?access_token={access_token}&role={role}")

@account_route.route('/logout')
def logout():
    #Xóa session để đăng xuất người dùng.
    session.clear()
    return redirect("/account")

@account_route.route('/')
def index():
    return "Hello world! <a href='/account/login'> <button>Login</button> </a>" 

@account_route.route('/protected_area')
@login_is_required
def protected_area():
    return "Protected! <a href='/account/logout'> <button>Logout</button> </a>"


