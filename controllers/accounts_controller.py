#logic
from bson import ObjectId
from flask import jsonify
from models import accounts, printers
from pymongo.errors import PyMongoError
from helper import accounts_helper
    
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
        cursor = printers.printers_collection().find({}, {
            "_id": 1,
        })

        history = list(cursor)
        
        for record in history: 
            record["report_history"] = [] 
            record["print_history"] = [] 

        data["paper_count"] = 0
        data["printer_history"] = history

    collection = accounts.accounts_collection()

    try:
        result = collection.insert_one(data)
        data["_id"] = str(data["_id"])
        for record in data["printer_history"]:
            record["_id"] = str(record["_id"])

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
            account['_id'] =  str(account['_id'])

            if account['role'] == "student":
                for record in account["printer_history"]:
                    record["_id"] = str(record["_id"])


            accounts_list.append(account)

        return accounts_list
    
    except PyMongoError as e:
        print(str(e))
        return ''
