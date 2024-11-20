from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

def start_server(route, my_host, my_port):
    app.register_blueprint(route)
    app.run(host=my_host, port=my_port, debug=True)