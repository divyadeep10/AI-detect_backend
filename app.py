import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure the API
API_KEY = os.getenv("GEMINI_API_KEY")
print(API_KEY , "API_KEY")
# if not API_KEY:
#     raise EnvironmentError("GEMINI_API_KEY environment variable is missing.")
genai.configure(api_key=API_KEY)
# genai.configure(api_key="AIzaSyBrTffN_pC2QL_BFJQ__TCUHHIXFxOP6wI")
# Initialize the generative model
model = genai.GenerativeModel("gemini-1.5-flash")

# Utility Functions
def generate_response(prompt):
    """
    Generates a response from the generative AI model.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Error generating response: {str(e)}")

def format_prompt(template, **kwargs):
    """
    Formats a prompt template with the provided keyword arguments.
    """
    return template.format(**kwargs)

# Prompt Templates
PROMPT_TEMPLATES = {
    "detect_language": "Given the following code snippet, detect the programming language and provide its name:\nCode:\n{code}",
    "explain_code": "Explain the following code snippet in simple terms. Assume the code is written in particular language find that and.\nCode:\n{code}",
    "optimize_code": "Analyze the following code snippet and suggest optimizations to improve performance, readability, or maintainability:\nCode:\n{code}",
    "refactor_code": "Refactor the following code snippet to make it more efficient, readable, and maintainable:\nCode:\n{code}",
    "debug_code": "Analyze the following code snippet and identify potential issues or bugs. Suggest debugging strategies to resolve them:\nCode:\n{code}",
    "check_style": "Check the following code snippet for compliance with the {style_guide} style guide. List any deviations and suggest corrections:\nCode:\n{code}",
    "best_practices": "Provide a list of best practices for writing clean and efficient code for code in: \nCode:\n{code}.",
    "generate_comments": "Generate inline comments for the following code snippet to make it more understandable:\nCode:\n{code}"
}

# Routes
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the AI-powered Code Analysis API!",
        "endpoints": [
            "/detect-language",
            "/explain-code",
            "/suggest-optimizations",
            "/refactor-code",
            "/debug-code",
            "/check-code-style",
            "/best-practices",
            "/generate-comments"
        ]
    })

@app.route('/detect-language', methods=['POST'])
def detect_language():
    code = request.json.get('code', '')
    if not code:
        return jsonify({"error": "Code is required"}), 400
    
    prompt = format_prompt(PROMPT_TEMPLATES["detect_language"], code=code)
    try:
        language = generate_response(prompt)
        return jsonify({"language": language})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/explain-code', methods=['POST'])
def explain_code():
    data = request.json
    code = data.get('code', '')
    language = data.get('language', '')

    if not code :
        return jsonify({"error": "Both code and language are required"}), 400

    prompt = format_prompt(PROMPT_TEMPLATES["explain_code"], code=code, language=language)
    try:
        explanation = generate_response(prompt)
        return jsonify({"explanation": explanation})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/suggest-optimizations', methods=['POST'])
def suggest_optimizations():
    code = request.json.get('code', '')
    if not code:
        return jsonify({"error": "Code is required"}), 400

    prompt = format_prompt(PROMPT_TEMPLATES["optimize_code"], code=code)
    try:
        optimizations = generate_response(prompt)
        return jsonify({"optimizations": optimizations})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/refactor-code', methods=['POST'])
def refactor_code():
    code = request.json.get('code', '')
    if not code:
        return jsonify({"error": "Code is required"}), 400

    prompt = format_prompt(PROMPT_TEMPLATES["refactor_code"], code=code)
    try:
        refactored_code = generate_response(prompt)
        return jsonify({"refactored_code": refactored_code})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/debug-code', methods=['POST'])
def debug_code():
    code = request.json.get('code', '')
    if not code:
        return jsonify({"error": "Code is required"}), 400

    prompt = format_prompt(PROMPT_TEMPLATES["debug_code"], code=code)
    try:
        debug_suggestions = generate_response(prompt)
        return jsonify({"debug_suggestions": debug_suggestions})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check-code-style', methods=['POST'])
def check_code_style():
    data = request.json
    code = data.get('code', '')
    style_guide = data.get('style_guide', 'PEP 8')

    if not code:
        return jsonify({"error": "Code is required"}), 400

    prompt = format_prompt(PROMPT_TEMPLATES["check_style"], code=code, style_guide=style_guide)
    try:
        style_violations = generate_response(prompt)
        return jsonify({"style_violations": style_violations})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/best-practices', methods=['POST'])
def best_practices():
    code = request.json.get('code', '')
    if not code:
        return jsonify({"error": "Programming code is required"}), 400

    prompt = format_prompt(PROMPT_TEMPLATES["best_practices"], code=code)
    try:
        practices = generate_response(prompt)
        return jsonify({"best_practices": practices})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-comments', methods=['POST'])
def generate_comments():
    code = request.json.get('code', '')
    if not code:
        return jsonify({"error": "Code is required"}), 400

    prompt = format_prompt(PROMPT_TEMPLATES["generate_comments"], code=code)
    try:
        comments = generate_response(prompt)
        return jsonify({"comments": comments})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run()
