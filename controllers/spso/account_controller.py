from bson import ObjectId
from flask import jsonify
from models import accounts
from pymongo.errors import PyMongoError
from helper import helper

def get_accounts_by_role(role):
    if not role:
        return jsonify({
            "status": "error",
            "message": "Role is required"
        }), 400
    
    if role not in ["student", "spso"]:
        return jsonify({
            "status": "error",
            "message": "Invalid role. Valid roles are 'student' and 'spso'."
        }), 400
    
    try:
        collection = accounts.accounts_collection()
        accounts_list = []

        for account in collection.find({"role": role}):
            account = helper.convert_objectid_to_string(account)
            accounts_list.append(account)

        return jsonify({
            "status": "success",
            "data": accounts_list
        }), 200
    
    except PyMongoError as e:
        print(str(e))
        return ''