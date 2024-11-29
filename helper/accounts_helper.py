import re

from bson import ObjectId
from models import accounts
from flask import jsonify

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, email):
        return True
    else: 
        return False
    
def check_available_mail(email):
    collection = accounts.accounts_collection()

    result = collection.find_one({
        "email": email,
    })

    if result:
        return True
    else:
        return False
    
def check_is_student(student_id):
    if not student_id:
        return False, jsonify({
            "status": "error",
            "message": "All fields are required: student ID and page."
        }), 400

    student = accounts.accounts_collection().find_one({"_id": ObjectId(student_id), "role": "student"})
    
    if student is None:
        return False, jsonify({"status": "error", "message": "Student not found."}), 404
    if student["role"] != "student":
        return False, jsonify({"status": "error", "message": "The account role is not 'student'."}), 403
    
    return True, None
