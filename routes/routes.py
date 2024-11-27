from routes import accounts
from routes.spso import printers as spso_printers
from routes.spso import accounts as spso_accounts
from routes import students

def get_all_routes():
    routes = [accounts.account_tuple, spso_printers.spso_printers_tuple, students.students_tuple, spso_accounts.spso_accounts_tuple]
    return routes 

