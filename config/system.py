from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

def start_server(routes, my_host, my_port, key):
    app.secret_key = key
    
    for route in routes:
        blueprint, prefix = route
        app.register_blueprint(blueprint, url_prefix=prefix)

    # In ra tất cả các route đã đăng ký 
    print("\nRegistered Routes:") 
    for rule in app.url_map.iter_rules(): 
        print(f"Endpoint: {rule.endpoint}, URL: {rule}")

    app.run(host=my_host, port=my_port, debug=True)