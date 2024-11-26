from bson import ObjectId
from flask import jsonify, request
from models import printers
from pymongo.errors import PyMongoError

def create_printer(data):
    try:
        name = data.get('name')
        model = data.get('model')
        type = data.get('type')
        location = data.get('location')
        status = data.get('status')
        manufacturer = data.get('manufacturer')
        purchase_date = data.get('purchase_date')
        print_count = 0
        paper_count = data.get('paper_count')
        maintenance_history = []
        ink = data.get('ink')

        if not all([name, model, type, location, status, manufacturer, purchase_date, paper_count, ink]):
            return jsonify({
                "status": "error", 
                "message": "All fields are required"
            }), 400

        printer_data = { 
            "_id": ObjectId(),
            "name": name, 
            "model": model, 
            "type": type, 
            "location": location, 
            "status": status, 
            "manufacturer": manufacturer, 
            "purchase_date": purchase_date,
            "print_count": print_count, 
            "paper_count": paper_count, 
            "maintenance_history": maintenance_history, 
            "ink": ink
        }

        collection = printers.printers_collection()
        result = collection.insert_one(data)
        data["_id"] = str(data["_id"])

        return jsonify({
            "status": "success",
            "data": data
        }), 201
    
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def get_printer(printer_id):
    try:
        printer = printers.printers_collection().find_one({
            "_id": ObjectId(printer_id)
        })
        
        if not printer:
            return jsonify({
                "status": "error",
                "message": f"No printer found with ID {printer_id}."
            }), 404
        
        # Chuyển đổi ObjectId thành chuỗi 
        printer['_id'] = str(printer['_id'])

        return jsonify({
            "status": "success",
            "data": printer
        }), 200

    except PyMongoError as e:
        print(str(e))
        return ''
    
def get_all_printers():
    try:
        collection = printers.printers_collection()
        printer_list = []

        for printer in collection.find():
            printer['_id'] =  str(printer['_id'])
            printer_list.append(printer)

        return printer_list 
    except PyMongoError as e:
        print(str(e))
        return ''

def delete_printer(printer_id):
    try:
        collection = printers.printers_collection()
        result = collection.delete_one({"_id": ObjectId(printer_id)})

        if result.deleted_count == 1:
            return jsonify({
                "status": "success",
                "message": f"Printer with ID {printer_id} has been deleted."
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"No printer found with ID {printer_id}."
            }), 404
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
def update_printer(printer_id, data):
    try:
        collection = printers.printers_collection()
        update_data = {}
        for key in data:
            if data[key] is not None:
                update_data[key] = data[key]

        result = collection.update_one(
            {"_id": ObjectId(printer_id)},
            {"$set": update_data}
        )

        if result.matched_count == 1:
            return jsonify({
                "status": "success",
                "message": f"Printer with ID {printer_id} has been updated."
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"No printer found with ID {printer_id}."
            }), 404
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def report_issue(printer_id, issue_description):
    try:
        collection = printers.printers_collection()
        result = collection.update_one(
            {"_id": ObjectId(printer_id)},
            {"$push": {"maintenance_history": {"issue": issue_description, "status": "reported"}}}
        )

        if result.matched_count == 1:
            return jsonify({
                "status": "success",
                "message": f"Issue reported for printer with ID {printer_id}."
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"No printer found with ID {printer_id}."
            }), 404
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500





