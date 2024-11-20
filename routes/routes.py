from flask import Blueprint
from flask_cors import CORS
from controllers import controller

route = Blueprint('tracker_route', __name__)
CORS(route, supports_credentials=True, origins=["http://localhost:3000"]) #link toi fe

def get_route():
    return route

@route.route('/hello', methods=['GET'])
def hello():
    return controller.hello()