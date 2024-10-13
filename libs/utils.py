import json
from functools import wraps
from flask import jsonify, request

# Decorator to handle JSON output and customize error messages
def handle_json_output(json_error_message=None):
    # Define the decorator function
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if the request content type is JSON
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400

            try:
                # Execute the decorated function
                result = f(*args, **kwargs)
                # If result is a JSON string, parse it before returning
                if isinstance(result, str):
                    return json.loads(result)
                return result
            except json.JSONDecodeError:
                # Return a custom or default error message if JSON decoding fails
                error_msg = json_error_message or "Invalid JSON format"
                return jsonify({"error": error_msg}), 400

        return decorated_function
    return decorator

# Decorator to validate the presence of required keys in the JSON input
def validate_json_input(keys=[]):
    # Define the decorator function
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Ensure that there are keys to validate
            if len(keys) == 0:
                raise ValueError("No keys provided to validate")

            # List to store any missing fields
            fields = []
            # Retrieve JSON data from the request
            data = request.get_json()
            # Check for each required key in the JSON data
            for key in keys:
                if not data.get(key):
                    fields.append(key)
            
            # If there are missing fields, return an error message with details
            if len(fields) > 0:
                return jsonify({
                    "error": {
                        "message": "Please provide all required fields",
                        "fields": fields
                    }
                }), 400
            
            # Proceed with the decorated function if validation passes
            return f(*args, **kwargs)

        return decorated_function
    return decorator
