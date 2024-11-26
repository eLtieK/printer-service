import os
from dotenv import load_dotenv
from flask import Blueprint, request
from flask_cors import CORS
from controllers.spso import printers_controller 
from middlewares import auth

load_dotenv()
SPSO_PREFIX = os.getenv('SPSO_PREFIX')

spso_printer_tuple = (Blueprint('spso_printer_route', __name__), f'/{SPSO_PREFIX}/printer')
spso_printer_route, prefix_route = spso_printer_tuple
CORS(spso_printer_route, supports_credentials=True, origins=["http://localhost:3000"]) #link toi fe

@spso_printer_route.route('/', methods=['POST'])
@auth.spso_is_required
def create_printer():
    data = request.get_json()
    return printers_controller.create_printer(data)

@spso_printer_route.route('/', methods=['GET'])
@auth.spso_is_required
def get_all_printers():
    return printers_controller.get_all_printers()

@spso_printer_route.route('/<printer_id>', methods=['GET'])
@auth.spso_is_required
def get_printer(printer_id):
    return printers_controller.get_printer(printer_id)

@spso_printer_route.route('/<printer_id>', methods=['DELETE'])
@auth.spso_is_required
def delete_printer(printer_id):
    return printers_controller.delete_printer(printer_id)

@spso_printer_route.route('/<printer_id>', methods=['PATCH'])
@auth.spso_is_required
def update_printer(printer_id):
    data = request.get_json()
    return printers_controller.update_printer(printer_id, data)