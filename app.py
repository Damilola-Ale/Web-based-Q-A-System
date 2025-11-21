import os
import string
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

def get_llm_response(question):
    """
    Sends the question to the Gemini API and returns the response.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        return "Error: GEMINI_API_KEY not found or not set in .env file."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error communicating with LLM API: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    # Preprocess (optional, but good for consistency with CLI)
    # question = question.lower() 
    
    answer = get_llm_response(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
