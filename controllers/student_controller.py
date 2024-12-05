from datetime import datetime
from bson import ObjectId
from flask import jsonify
from models import printers, accounts
from pymongo.errors import PyMongoError
from helper import printers_help, accounts_helper
from controllers import accounts_controller
from controllers.spso import printer_controller

def add_page(student_id, page):
    try:
        result = accounts_helper.check_is_student(student_id)
        if(not result[0]):
            return result[1], result[2]

        accounts.accounts_collection().update_one(
            {"_id": ObjectId(student_id)},
            {
                "$inc": {"paper_count": +page}
            }
        )
        return jsonify({
            "status": "success", 
            "message": "Pages added successfully."
        }), 200
    
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
def report_issue(student_id, printer_id, issue):
    try:
        if not printer_id or not issue or not student_id:
            return jsonify({
                "status": "error",
                "message": "All fields are required: Printer ID, issue description, student ID, and date."
            }), 400
        
        printer_result = printers_help.check_is_printer(printer_id)
        if(not printer_result[0]):
            return printer_result[1], printer_result[2]
        
        student_result = accounts_helper.check_is_student(student_id)
        if(not student_result[0]):
            return student_result[1], student_result[2]
        
        printer_collection = printers.printers_collection()
        student_collection = accounts.accounts_collection()

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        student_data = accounts_controller.get_account_data(student_id)
        # Cập nhật báo cáo trong printer collection
        result_printer = printer_collection.update_one(
            {"_id": ObjectId(printer_id)},
            {"$push": {
                "report_history": {
                    "student_id": ObjectId(student_id),
                    "name": student_data["name"],
                    "email": student_data["email"],
                    "issue": issue, 
                    "date": date
                }}}
        )

        # Cập nhật báo cáo trong student collection
        printer_data = printer_controller.get_printer_name_location(printer_id)
        result_student = student_collection.update_one(
            {"_id": ObjectId(student_id)},
            {"$push": {
                "report_history": {
                    "printer_id": ObjectId(printer_id),
                    "name": printer_data["name"],
                    "location": printer_data["location"],
                    "issue": issue, 
                    "date": date
                }}}
        )

        return jsonify({
            "status": "success",
            "message": f"Reported issue for printer {printer_id} by student {student_id}."
        }), 200
        
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
def print_document(printer_id, student_id, file_name, page_count):
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
        
        # Validate printer and student existence
        printer_result = printers_help.check_is_printer(printer_id)
        if(not printer_result[0]):
            return printer_result[1]
        
        student_result = accounts_helper.check_is_student(student_id)
        if(not student_result[0]):
            return student_result[1]
        
        printer = printers.printers_collection().find_one({"_id": ObjectId(printer_id)})
        student = accounts.accounts_collection().find_one({"_id": ObjectId(student_id)})
        
        # Check printer status
        if printer["status"] != "Enabled":
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
        student_data = accounts_controller.get_account_data(student_id)
        printer_entry = {
            "file_name": file_name,
            "pages": page_count,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "student_id": ObjectId(student_id),
            "name": student_data["name"],
            "email": student_data["email"]
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
        printer_data = printer_controller.get_printer_name_location(printer_id)
        student_entry = {
            "file_name": file_name,
            "pages": page_count,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "printer_id": ObjectId(printer_id),
            "name": printer_data["name"],
            "location": printer_data["location"]
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
