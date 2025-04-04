import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from NuAnswers import AccountingFinanceTutor

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the tutor
tutor = AccountingFinanceTutor()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the message from the request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        user_message = data['message']
        
        # Get response from tutor
        tutor_response = tutor.evaluate_response(user_message, tutor.current_topic)
        
        # Return the response as JSON
        return jsonify({
            "response": tutor_response,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
