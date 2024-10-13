from flask import Flask, jsonify, request
from libs.model import Nutritionist
from libs.utils import handle_json_output, validate_json_input

# Initialize the Flask application
app = Flask(__name__)

# Instantiate the Nutritionist class
nutritionist = Nutritionist()

# Define the '/analyze' route, which accepts POST requests for ingredient analysis
@app.route('/analyze', methods=['POST'])
# Decorator to handle JSON output and customize error messages
@handle_json_output(json_error_message=nutritionist.model_response_error)
# Decorator to validate JSON input, ensuring 'ingredients' key is present
@validate_json_input(keys=['ingredients'])
def analyze_ingredients():
    # Retrieve JSON data from the request
    data = request.get_json()
    ingredients = data.get('ingredients')

    # Check if ingredients are provided, return an error if missing
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    # Process ingredients using the Nutritionist model and return the analysis
    return nutritionist.get_advice_from_ingredients(ingredients)

# Run the application on port 3000 in debug mode
if __name__ == '__main__':
    app.run(port=3000, debug=True)
