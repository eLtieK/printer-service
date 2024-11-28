from datetime import datetime
from bson import ObjectId
from flask import jsonify
from models import printers, accounts
from pymongo.errors import PyMongoError
from helper import printers_help

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
                    "student_id": ObjectId(student_id),
                    "issue": issue, 
                    "date": date
                }}}
        )

        # Cập nhật báo cáo trong student collection
        result_student = student_collection.update_one(
            {"_id": ObjectId(student_id)},
            {"$push": {
                "report_history": {
                    "printer_id": ObjectId(printer_id),
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
    
def print(printer_id, student_id, file_name, page_count):
    try:
        # Fetch printer and student data from the database
        if not printer_id or not file_name or not student_id or not page_count:
            return jsonify({
                "status": "error",
                "message": "All fields are required: Printer ID, student ID, file name and page count."
            }), 400
        
        if not printers_help.check_valid_page_count(page_count):
            return jsonify({
                "status": "error",
                "message": "Page count must be a positive integer."
            }), 400

        printer = printers.printers_collection().find_one({"_id": ObjectId(printer_id)})
        student = accounts.accounts_collection().find_one({"_id": ObjectId(student_id)})
        
        # Validate printer and student existence
        if not printer:
            return jsonify({"status": "error", "message": "Printer not found."}), 404
        if not student:
            return jsonify({"status": "error", "message": "Student not found."}), 404
        if student["role"] != "student":
            return jsonify({"status": "error", "message": "The account role is not 'student'."}), 403
        
        # Check printer status
        if printer["status"] != "Ready":
            return jsonify({"status": "error", "message": f"Printer is not ready: {printer['status']}."}), 400
        
        # Check paper availability
        if printer["paper_count"] < page_count:
            return jsonify({"status": "error", "message": "Not enough paper in the printer."}), 400
        
        # Check ink level
        if not printers_help.is_sufficient_ink(printer["ink"], page_count):
            return jsonify({"status": "error", "message": "Printer ink level is too low."}), 400
        
        #Check student paper
        if student["paper_count"] < page_count:
            return jsonify({"status": "error", "message": "Not enough paper in the student's account."}), 400

        # Update printer and student data
        # Update printer data
        printer_entry = {
            "file_name": file_name,
            "pages": page_count,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "student_id": ObjectId(student_id)
        }
        ink_to_use = printers_help.calculate_ink_usage(printer["ink"], page_count)
        printers.printers_collection().update_one(
            {"_id": ObjectId(printer_id)},
            {
                "$inc": {
                    "paper_count": -page_count, # Deduct paper count
                    "ink.level": -ink_to_use
                },  
                "$push": {"print_history": printer_entry}  # Add to print history
            }
        )

        # Update student print history
        student_entry = {
            "file_name": file_name,
            "pages": page_count,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "printer_id": ObjectId(printer_id)
        }
        accounts.accounts_collection().update_one(
            {"_id": ObjectId(student_id)},
            {
                "$inc": {"paper_count": -page_count},
                "$push": {"print_history": student_entry}
            }
        )

        # Return success response
        return jsonify({"status": "success", "message": "Document printed successfully."}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"status": "error", "message": str(e)}), 500
