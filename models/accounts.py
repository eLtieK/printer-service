from models import init_model as model

def accounts_collection():
    return model.init_collection("accounts")