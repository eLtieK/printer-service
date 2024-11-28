import re

from bson import ObjectId
from models import accounts
from flask import jsonify

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, email):
        return True
    else: 
        return False
    
def check_available_mail(email):
    collection = accounts.accounts_collection()

    result = collection.find_one({
        "email": email,
    })

    if result:
        return True
    else:
        return False
    
