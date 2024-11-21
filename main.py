from dotenv import load_dotenv
from config import system
import os
from routes import routes

if __name__ == "__main__":
    # Load các biến môi trường từ file .env
    load_dotenv()
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    key = os.getenv('KEY')

    system.start_server(routes.get_all_routes(), host, port, key)