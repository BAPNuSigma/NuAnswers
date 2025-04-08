import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

# Get Anthropic API key
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: ANTHROPIC_API_KEY is not set! Check your environment variables.")

# Initialize Claude client
client = anthropic.Anthropic(api_key=api_key)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_claude_response(user_prompt):
    """Function to get response from Claude API"""
    try:
        print("⚡ Sending request to Claude...")
        print(f"📨 Prompt: {user_prompt}")
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=0.7,
            messages=[{"role": "user", "content": user_prompt}]
        )
        print("✅ Received response from Claude")
        return response.content[0].text
    except Exception as e:
        print(f"❌ Error while calling Claude: {str(e)}")
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the message from the request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        user_message = data['message']
        
        # Get response from Claude
        tutor_response = get_claude_response(user_message)
        
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
