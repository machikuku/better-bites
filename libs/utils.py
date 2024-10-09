import json
from functools import wraps
from flask import jsonify, request

def handle_json_output(json_error_message=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
            
            try:
                result = f(*args, **kwargs)
                if isinstance(result, str):
                    return json.loads(result)
                return result
            except json.JSONDecodeError:
                error_msg = json_error_message or "Invalid JSON format"
                return jsonify({"error": error_msg}), 400
            
        return decorated_function
    return decorator

def validate_json_input(keys=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if len(keys) == 0:
                raise ValueError("No keys provided to validate")

            fields = []
            data = request.get_json()
            for key in keys:
                if not data.get(key):
                    fields.append(key)
            
            if len(fields) > 0:
                return jsonify({"error": { "message": "Please provide all required fields", "fields": fields }}), 400
            
            return f(*args, **kwargs)

        return decorated_function
    return decorator