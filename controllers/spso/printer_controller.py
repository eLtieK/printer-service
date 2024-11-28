from bson import ObjectId
from flask import jsonify
from models import printers, accounts
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta
from helper import helper

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
        report_history = []
        print_history = []
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
            "report_history": report_history,
            "print_history": print_history,
            "ink": ink
        }

        collection = printers.printers_collection()
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
        printer = helper.convert_objectid_to_string(printer)

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
            printer = helper.convert_objectid_to_string(printer)
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

def export_printing_report(printer_id, student_id, date_range, start_date, end_date):
    try:
        query = {}
        if printer_id:
            query["_id"] = ObjectId(printer_id)
        if student_id:
            query["print_history.student_id"] = ObjectId(student_id)
        
        if date_range == 'daily':
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
        elif date_range == 'weekly':
            start_date = datetime.now() - timedelta(days=datetime.now().weekday())
            end_date = start_date + timedelta(days=7)
        elif date_range == 'monthly':
            start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = (start_date + timedelta(days=32)).replace(day=1)
        elif start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid date range or custom dates."
            }), 400
        query["print_history.date"] = {"$gte": start_date.strftime("%Y-%m-%d %H:%M:%S"), "$lt": end_date.strftime("%Y-%m-%d %H:%M:%S")}
        
        printers_data = printers.printers_collection().find(query)
        report = []
        
        for printer in printers_data:
            printer_report = {
                "printer_id": printer['_id'],
                "name": printer['name'],
                "model": printer['model'],
                "location": printer['location'],
                "total_pages_printed": sum(job['pages'] for job in printer['print_history']),
                "total_print_jobs": len(printer['print_history']),
                "print_history": printer['print_history']
            }
            printer_report = helper.convert_objectid_to_string(printer_report)
            report.append(printer_report)
        
        return jsonify({
            "status": "success",
            "data": report
        }), 200

    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500