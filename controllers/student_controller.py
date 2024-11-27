from datetime import datetime
from bson import ObjectId
from flask import jsonify
from models import printers, accounts
from pymongo.errors import PyMongoError

def report_issue(student_id, printer_id, issue):
    try:
        if not printer_id or not issue or not student_id:
            return jsonify({
                "status": "error",
                "message": "All fields are required: Printer ID, issue description, student ID, and date."
            }), 400
        
        printer_collection = printers.printers_collection()
        student_collection = accounts.accounts_collection()

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Cập nhật báo cáo trong printer collection
        result_printer = printer_collection.update_one(
            {"_id": ObjectId(printer_id)},
            {"$push": {
                "report_history": {
                    "issue": issue, 
                    "date": date
                }}}
        )

        # Cập nhật báo cáo trong student collection
        result_student = student_collection.update_one(
            {"_id": ObjectId(student_id),
             "printer_history._id": ObjectId(printer_id)},
            {"$push": {
                "printer_history.$.report_history": {
                    "issue": issue, 
                    "date": date
                }}}
        )

        if result_printer.matched_count == 1 and result_student.matched_count == 1:
            return jsonify({
                "status": "success",
                "message": f"Reported issue for printer {printer_id} by student {student_id}."
            }), 200
        elif result_printer.matched_count == 0:
            return jsonify({
                "status": "error",
                "message": f"Printer with ID {printer_id} not found."
            }), 404
        elif result_student.matched_count == 0:
            return jsonify({
                "status": "error",
                "message": f"Student with ID {student_id} not found or printer {printer_id} not in student's history."
            }), 404
        
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
# def print(printer_id, student_id, name, pages):
#     try
