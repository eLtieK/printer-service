from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

def start_server(routes, my_host, my_port, key):
    app.secret_key = key
    
    for route in routes:
        app.register_blueprint(route)

    app.run(host=my_host, port=my_port, debug=True)