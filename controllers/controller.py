#logic
from flask import jsonify

def hello():
    return jsonify({
        "message": "hello",
    }), 201