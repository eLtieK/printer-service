from bson import ObjectId
from flask import jsonify
from models import printers, accounts
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta
from helper import accounts_helper, helper, printers_help

def get_printer_name_location(id):
    try:
        collection = printers.printers_collection()
        printer = collection.find_one({
            "_id": ObjectId(id)
        })

        return {
            "name": printer["name"],
            "location": printer["location"]
        }
    
    except PyMongoError as e:
        print(str(e))
        return ''

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
            if 'paper_price' in printer:
                continue  # Skip this printer
            
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
    
def update_paper_price(money):
    collection = printers.printers_collection()

    result = collection.update_one(
        {"paper_price": {"$exists": True}},  # Điều kiện tìm kiếm
        {"$set": {"paper_price": money}}     # Thay đổi giá trị
    )

    if result.matched_count == 0:
        data = {"paper_price": money}
        collection.insert_one(data)

    return jsonify({
            "status": "success",
            "message": f"Updated page price."
        }), 200

def get_paper_price():
    collection = printers.printers_collection()
    result = collection.find_one(
        {"paper_price": {"$exists": True}}  # Điều kiện tìm kiếm
    )
    
    if result is None:
        return 0
    
    return result["paper_price"]


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
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        elif not date_range: 
            start_date = datetime.min
            end_date = datetime.now()
        elif date_range == 'daily':
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
        elif date_range == 'weekly':
            start_date = datetime.now() - timedelta(days=datetime.now().weekday())
            end_date = start_date + timedelta(days=7)
        elif date_range == 'monthly':
            start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = (start_date + timedelta(days=32)).replace(day=1)
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid date range."
            }), 400

        if start_date and end_date:
            query["print_history.date"] = {"$gte": start_date.strftime("%Y-%m-%d %H:%M:%S"), "$lt": end_date.strftime("%Y-%m-%d %H:%M:%S")}
        
        printers_data = printers.printers_collection().find(query)
        report = []
        total_pages_printed = 0
        
        for printer in printers_data:
            printer_name = printer["name"] 
            printer_location = printer["location"] 
            printer_id_data = printer["_id"] 
            for history in printer['print_history']:
                # printer_report = {
                #     "printer_id": printer['_id'],
                #     "name": printer['name'],
                #     "model": printer['model'],
                #     "location": printer['location'],
                #     "total_pages_printed": total_pages,
                #     "total_print_jobs": len(printer['print_history']),
                #     "print_history": printer['print_history']
                # }
                history["printer name"] = printer_name
                history["printer location"] = printer_location
                history["printer_id"] = printer_id_data
                printer_report = helper.convert_objectid_to_string(history)
                report.append(printer_report)
        
        return jsonify({
            "status": "success",
            "report": report,
        }), 200

    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def get_all_issues(date_range=None, start_date=None, end_date=None):
    try:
        query = {"report_history": {"$exists": True, "$ne": []}}
        
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        elif date_range == 'daily':
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
        elif date_range == 'weekly':
            start_date = datetime.now() - timedelta(days=datetime.now().weekday())
            end_date = start_date + timedelta(days=7)
        elif date_range == 'monthly':
            start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = (start_date + timedelta(days=32)).replace(day=1)
        else: 
            start_date = datetime.min
            end_date = datetime.now()
        if start_date and end_date:
            query["report_history.date"] = {"$gte": start_date.strftime("%Y-%m-%d %H:%M:%S"), "$lt": end_date.strftime("%Y-%m-%d %H:%M:%S")}
        
        issues = []
        printers_data = printers.printers_collection().find(query)
        for printer in printers_data:
            for report in printer["report_history"]:
                issues.append({
                    "printer_id": str(printer["_id"]),
                    "student_id": str(report["student_id"]),
                    "issue": report["issue"],
                    "date": report["date"],
                    "student name": report["name"],
                    "student email": report["email"],
                    "printer name": printer["name"],
                    "printer location": printer["location"],
                })
        return jsonify({"status": "success", "data": issues}), 200
    except PyMongoError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def update_maintenance_history(printer_id, spso_id, data):
    try:
        if(not printer_id or not spso_id or not data.get("details")):
            return jsonify({
                "status": "error",
                "message": "All fields are required: SPSO ID, and details."
            }), 400
        
        printer_result = printers_help.check_is_printer(printer_id)
        if(not printer_result[0]):
            return printer_result[1], printer_result[2]
        
        spso_result = accounts_helper.check_is_spso(spso_id)
        if(not spso_result[0]):
            return spso_result[1], spso_result[2]
        
        maintenance_entry_printer = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": data.get("details"),
            "spso_id": ObjectId(spso_id)
        }
        result_printer = printers.printers_collection().update_one(
            {"_id": ObjectId(printer_id)},
            {"$push": {"maintenance_history": maintenance_entry_printer}}
        )

        maintenance_entry_spso = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": data.get("details"),
            "printer_id": ObjectId(printer_id)
        }

        result_spso = accounts.accounts_collection().update_one(
            {"_id": ObjectId(spso_id)},
            {"$push": {"maintenance_history": maintenance_entry_spso}}
        )

        return jsonify({
            "status": "success",
            "message": f"Updated maintenance history for printer {printer_id}."
        }), 200
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)}
        ), 500

def get_maintenance_history(printer_id, date_range=None, start_date=None, end_date=None):
    try:
        query = {"_id": ObjectId(printer_id)}
        
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        elif date_range == 'daily':
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
        elif date_range == 'weekly':
            start_date = datetime.now() - timedelta(days=datetime.now().weekday())
            end_date = start_date + timedelta(days=7)
        elif date_range == 'monthly':
            start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = (start_date + timedelta(days=32)).replace(day=1)
        else:
            start_date = datetime.min
            end_date = datetime.now()
        
        if start_date and end_date:
            query["maintenance_history.date"] = {"$gte": start_date.strftime("%Y-%m-%d %H:%M:%S"), "$lt": end_date.strftime("%Y-%m-%d %H:%M:%S")}
        
        printer = printers.printers_collection().find_one({"_id": ObjectId(printer_id)})
        if not printer:
            return jsonify({
                "status": "error",
                "message": f"No printer found with ID {printer_id}."
            }), 404
        
        maintenance_history = [
            entry for entry in printer.get("maintenance_history", [])
            if start_date <= datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S") < end_date
        ]
        
        maintenance_history = helper.convert_objectid_to_string(maintenance_history)
        return jsonify({
            "status": "success",
            "data": maintenance_history
        }), 200
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500