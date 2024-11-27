from routes import accounts
from routes.spso import printers
from routes.student import students

def get_all_routes():
    routes = [accounts.account_tuple, printers.spso_printer_tuple, students.students_bp_tuple]
    return routes 

