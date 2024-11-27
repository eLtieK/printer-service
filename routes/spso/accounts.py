import os
from dotenv import load_dotenv
from flask import Blueprint, request
from flask_cors import CORS
from controllers.spso import account_controller 
from middlewares.auth import login_is_required, spso_is_required
import pathlib

load_dotenv(dotenv_path= pathlib.Path(__file__).parent.parent.parent / '.env')
SPSO_PREFIX = os.getenv('SPSO_PREFIX')

spso_accounts_tuple = (Blueprint('spso_accounts_route', __name__), f'/{SPSO_PREFIX}/account')
spso_accounts_route, prefix_route = spso_accounts_tuple
CORS(spso_accounts_route, supports_credentials=True, origins=["http://localhost:3000"]) #link toi fe

@spso_accounts_route.route('/', methods=['GET'])
@login_is_required
@spso_is_required
def get_accounts_by_role():
    data = request.get_json() 
    role = data.get('role') 
    
    return account_controller.get_accounts_by_role(role)