#logic
from bson import ObjectId
from flask import jsonify
from models import accounts, printers
from pymongo.errors import PyMongoError
from helper import accounts_helper, helper
    
def delete_account(email):
    try:
        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Xóa tài khoản bằng email
        result = accounts.accounts_collection().delete_one({"email": email})

        if result.deleted_count > 0:
            return jsonify({"message": "Account deleted successfully"}), 200
        else:
            return jsonify({"error": "Account not found"}), 404

    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


def create_or_alter_account(email, name, phone):
    if not email or not name or not phone: #Check xem format của request có đúng không
        return jsonify({
            "status": "error",
            "message": "Email, name and phone are required"
        }), 400
    
    
    # Get the accounts collection
    accounts_collection = accounts.accounts_collection()

    # Create or update the account
    try:
        result = accounts_collection.update_one(
            {"email": email},  # Query to find an account with the given email
            {"$set": {"name": name, "phone": phone}},  # Update or create the document
            upsert=True  # If no document matches, create one
        )

        if result.matched_count > 0:
            return jsonify({
                "status": "success",
                "message": "Account updated successfully"
            }), 200
        else:
            return jsonify({
                "status": "success",
                "message": "Account created successfully"
            }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500
    
def create_account(email, role):
    if not email or not role: #Check xem format của request có đúng không
        return jsonify({
            "status": "error",
            "message": "Email and role are required"
        }), 400
    
    if not accounts_helper.is_valid_email(email): #Check định dạng email
        return jsonify({
            "status": "error",
            "message": "Invalid email format"
        }), 400
    
    if accounts_helper.check_available_mail(email): #Check xem email đã được tạo cấp role chưa
        return jsonify({
            "status": "error",
            "message": "Email has already been registered"
        }), 400
    
    data = {
        "_id": ObjectId(),
        "email": email,
        "role": role
    }

    if (role == "student"):
        data["paper_count"] = 0
        data["print_history"] = []
        data["report_history"] = []
    
    if (role == "spso"):
        data["maintenance_history"] = []
        
    collection = accounts.accounts_collection()

    try:
        result = collection.insert_one(data)
        data = helper.convert_objectid_to_string(data)
        
        return jsonify({
            "status": "success",
            "data": data
        }), 201
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def get_account_role(email):
    try:
        data = accounts.accounts_collection().find_one({
            "email": email
        })

        if data and 'role' in data:
            return data['role']
        else:
            return 'guest'
    except PyMongoError as e:
        print(str(e))
        return ''
    
def get_all_accounts():
    try:
        collection = accounts.accounts_collection()
        accounts_list = []

        for account in collection.find():
            account = helper.convert_objectid_to_string(account)
            accounts_list.append(account)

        return accounts_list
    
    except PyMongoError as e:
        print(str(e))
        return ''
