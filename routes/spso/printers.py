import os
from dotenv import load_dotenv
from flask import Blueprint, request
from flask_cors import CORS
from controllers.spso import printers_controller 

load_dotenv()
SPSO_PREFIX = os.getenv('SPSO_PREFIX')

spso_printer_tuple = (Blueprint('spso_printer_route', __name__), f'/{SPSO_PREFIX}/printer')
spso_printer_route, prefix_route = spso_printer_tuple
CORS(spso_printer_route, supports_credentials=True, origins=["http://localhost:3000"]) #link toi fe

@spso_printer_route.route('/create', methods=['POST'])
def create_printer():
    data = request.get_json()
    return printers_controller.create_printer(data)