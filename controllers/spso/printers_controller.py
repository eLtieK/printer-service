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
        data.pop('_id', None)

        return jsonify({
            "status": "success",
            "data": data
        }), 201
    
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def get_all_printer():
    collection = printers.printers_collection()
    printer_list = []

    for printer in collection.find():
        printer_list.append(printer)

    return printer_list 


    
