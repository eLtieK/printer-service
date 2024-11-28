import os
from dotenv import load_dotenv
from flask import Blueprint, request
from flask_cors import CORS
from controllers.spso import printer_controller 
from middlewares.auth import login_is_required, spso_is_required
import pathlib

load_dotenv(dotenv_path= pathlib.Path(__file__).parent.parent.parent / '.env')
SPSO_PREFIX = os.getenv('SPSO_PREFIX')

spso_printers_tuple = (Blueprint('spso_printers_route', __name__), f'/{SPSO_PREFIX}/printer')
spso_printers_route, prefix_route = spso_printers_tuple
CORS(spso_printers_route, supports_credentials=True, origins=["http://localhost:3000"]) #link toi fe


@spso_printers_route.route('/', methods=['POST'])
@login_is_required
@spso_is_required
def create_printer():
    data = request.get_json()
    return printer_controller.create_printer(data)

@spso_printers_route.route('/', methods=['GET'])
@login_is_required
@spso_is_required
def get_all_printers():
    return printer_controller.get_all_printers()

@spso_printers_route.route('/<printer_id>', methods=['GET'])
@login_is_required
@spso_is_required
def get_printer(printer_id):
    return printer_controller.get_printer(printer_id)

@spso_printers_route.route('/<printer_id>', methods=['DELETE'])
@login_is_required
@spso_is_required
def delete_printer(printer_id):
    return printer_controller.delete_printer(printer_id)

@spso_printers_route.route('/<printer_id>', methods=['PATCH'])
@login_is_required
@spso_is_required
def update_printer(printer_id):
    data = request.get_json()
    return printer_controller.update_printer(printer_id, data)

@spso_printers_route.route('/export_printing_report', methods=['GET'])
@login_is_required
@spso_is_required
def export_printing_report():
    """
    Export printing report with optional filters and date ranges.
    
    Args:
        printer_id (str): Optional. ID of the printer to filter by.
        student_id (str): Optional. ID of the student to filter by.
        date_range (str): Optional. Date range for the report. Can be 'daily', 'weekly', 'monthly', or 'custom'.
        start_date (str): Optional. Start date for custom date range in 'YYYY-MM-DD' format.
        end_date (str): Optional. End date for custom date range in 'YYYY-MM-DD' format.
    """
    data = request.get_json()
    printer_id = data.get('printer_id')
    student_id = data.get('student_id')
    date_range = data.get('date_range', 'daily')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    return printer_controller.export_printing_report(printer_id, student_id, date_range, start_date, end_date)