import os
from dotenv import load_dotenv
from flask import Blueprint, request
from flask_cors import CORS
from controllers import student_controller, payment_controller
from controllers.spso import printer_controller
from middlewares.auth import student_is_required, login_is_required
import pathlib

load_dotenv(dotenv_path= pathlib.Path(__file__).parent.parent / '.env')
STUDENT_PREFIX = os.getenv('STUDENT_PREFIX')

students_tuple = (Blueprint('students_tuple', __name__), f'/{STUDENT_PREFIX}')
students_route, prefix_route = students_tuple
CORS(students_route, supports_credentials=True, origins=["http://localhost:3000"])

@students_route.route('/report_issue', methods=['POST'])
@login_is_required
@student_is_required
def report_issue():
    data = request.get_json()
    printer_id = data.get('printer_id')
    student_id = data.get('student_id')
    issue = data.get('issue')
    
    return student_controller.report_issue(student_id, printer_id, issue)

@students_route.route('/printer', methods=['GET'])
@login_is_required
@student_is_required
def get_all_printers():
    return printer_controller.get_all_printers()

@students_route.route('/printer/<printer_id>', methods=['GET'])
@login_is_required
@student_is_required
def get_printer(printer_id):
    return printer_controller.get_printer(printer_id)

@students_route.route('/print_document', methods=['POST'])
@login_is_required
@student_is_required
def print():
    data = request.get_json()
    printer_id = data.get('printer_id')
    student_id = data.get('student_id')
    file_name = data.get('file_name')
    page_count = data.get('page_count')
    return student_controller.print_document(printer_id, student_id, file_name, page_count)

@students_route.route('/add_page', methods=['POST'])
@login_is_required
@student_is_required
def add_page():
    data = request.get_json()
    student_id = data.get('student_id')
    page = data.get('page')
    return student_controller.add_page(student_id, page)
    
    