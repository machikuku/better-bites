from flask import jsonify
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Nutritionist class to handle nutrition advice using the Groq API
class Nutritionist:
    # Define the model to be used and an error message for invalid JSON responses
    MODEL = "llama3-70b-8192"
    model_response_error = "Model returned an invalid json response."

    def __init__(self):
        # Initialize the Groq API client with an API key from the environment variables
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Method to get nutritional advice based on a list of ingredients
    def get_advice_from_ingredients(self, ingredients):
        # Construct the prompt for the model
        prompt = f"""You are a nutritionist dietitian. Based on the following ingredients, identify which ingredients are suitable and which are unsuitable for the user's health profile. Additionally, provide Health Tips on how to make the food healthier by adding specific ingredients or nutrional advice. Your response must be in valid JSON format with the following structure:

{{
    "suitable_ingredients": [
        {{ "explanation": "Reason for suitability"}},
        {{ "explanation": "Reason for suitability"}}
    ],
    "unsuitable_ingredients": [
        {{"ingredient": "ingredient3", "reason": "Reason for unsuitability"}},
        {{"ingredient": "ingredient4", "reason": "Reason for unsuitability"}}
    ],
    "health_tips": [
        {{"suggestion": "Add ingredient5 for additional vitamins", "benefit": "Increases nutrient density"}},
        {{"suggestion": "Replace ingredient6 with a healthier alternative", "benefit": "Reduces unhealthy fats"}}
    ]
}}

If you cannot process the ingredients or encounter any issues, respond with a JSON object containing an 'error' key, like this:

{{
    "error": "Description of the error or issue encountered"
}}

Ensure your response can be parsed by Python's json.loads() function.

Ingredients: {ingredients}

JSON Response:"""

        try:
            # Use the Groq API client to generate a response from the AI model
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": "You are a nutritionist dietitian. Always respond in valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1,      # Controls response variability
                max_tokens=1024,    # Limits the length of the response
                top_p=1,            # Limits to top probable responses
                stream=False,       # Non-streaming mode
                stop=None,          # No specific stop sequence
            )

            # Print the model's response for debugging purposes
            print(response.choices[0].message.content)

            # Return the model's response as a string (assumes JSON format)
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Print the error for debugging and return a JSON error response
            print(e)
            return jsonify({"error": "Error encountered from Groq API"}), 500
