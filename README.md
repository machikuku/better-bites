# Better Bites Backend

This is the backend service for the Better Bites mobile application, which analyzes food ingredients and provides nutritional advice.

## Overview

The Better Bites mobile app allows users to take pictures of food ingredients. These images are converted to text and sent to this backend service. The backend then uses AI model (Llama 3) to analyze the ingredients and provide nutritional advice, health risks, and suggested complementary ingredients.

## Technologies Used

- Flask: Web framework for the API
- Groq: AI model for ingredient analysis (primary)
- Ollama: Alternative AI model (fallback)
- Python 3.12

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/better-bites-backend.git
   cd better-bites-be
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.sample` to `.env`
   - Add your Groq API key to the `.env` file:
     ```
     GROQ_API_KEY=your_api_key_here
     ```

## Getting a Groq API Key

1. Sign up for an account at [Groq's website](https://www.groq.com/).
2. Navigate to your account settings or API section.
3. Generate a new API key.
4. Copy the API key and paste it into your `.env` file.

## Running the Application

1. Ensure your virtual environment is activated.
2. Run the Flask application:
   ```
   python app.py
   ```
3. The server will start, typically on `http://localhost:3000`.

## API Endpoints

- `POST /analyze`: Accepts a JSON payload with an "ingredients" key containing the list of ingredients to analyze.

## Notes

- The Groq API is the primary model used but may sometimes be unavailable due to high demand.
- An alternative solution is to download and run a local model, but this may result in slower response times depending on the server specifications.
