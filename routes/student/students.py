import os
from dotenv import load_dotenv
from flask import Blueprint, request
from flask_cors import CORS
from controllers.spso import printers_controller
from middlewares.auth import student_is_required

load_dotenv()
STUDENT_PREFIX = os.getenv('STUDENT_PREFIX', 'student')

students_bp_tuple = (Blueprint('students_bp_tuple', __name__), f'/{STUDENT_PREFIX}')
students_bp, prefix_route = students_bp_tuple
CORS(students_bp, supports_credentials=True, origins=["http://localhost:3000"])

@students_bp.route('/report_issue', methods=['POST'])
# @student_is_required
def report_issue():
    data = request.get_json()
    printer_id = data.get('printer_id')
    issue_description = data.get('issue_description')
    result = printers_controller.report_issue(printer_id, issue_description)
    return result