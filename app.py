from flask import Flask, jsonify, request
from libs.model import Nutritionist
from libs.utils import handle_json_output, validate_json_input

app = Flask(__name__)
nutritionist = Nutritionist()

@app.route('/analyze', methods=['POST'])
@handle_json_output(json_error_message=nutritionist.model_response_error)
@validate_json_input(keys=['ingredients'])
def analyze_ingredients():
    data = request.get_json()
    ingredients = data.get('ingredients')

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    return nutritionist.get_advice_from_ingredients(ingredients)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
