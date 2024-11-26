from routes import accounts
from routes.spso import printers

def get_all_routes():
    routes = [accounts.account_tuple, printers.spso_printer_tuple]
    return routes 

