from flask import Blueprint, request, jsonify
from controllers.spso import printers_controller
from middlewares.auth import student_is_required
import os

students_bp = Blueprint('students', __name__)
student_prefix = os.getenv('STUDENT_PREFIX', 'student')

@students_bp.route(f'/{student_prefix}/report_issue', methods=['POST'])
@student_is_required
def report_issue():
    data = request.get_json()
    printer_id = data.get('printer_id')
    issue_description = data.get('issue_description')

    if not printer_id or not issue_description:
        return jsonify({
            "status": "error",
            "message": "Printer ID and issue description are required."
        }), 400

    result = printers_controller.report_issue(printer_id, issue_description)
    return result
