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
        
        # System prompt to guide Claude's behavior
        system_prompt = """You are an accounting and finance tutor. Your role is to help students understand and solve accounting problems effectively.

        GUIDELINES:
        1. Break down complex problems into clear, logical steps
        2. Explain concepts clearly and concisely
        3. Show calculations and reasoning when appropriate
        4. Use accounting terminology correctly
        5. Provide clear explanations of why certain steps are taken
        6. Help students understand the underlying principles
        7. Confirm correct answers and explain why they are correct
        8. For incorrect answers, explain the correct approach and why it's better

        Example of good tutoring:
        Student: "I need help with bond conversion."
        Tutor: "Let's solve this step by step. First, we need to calculate the total par value of the common stock being issued. We know we're issuing 3,000 shares, and each share has a par value of $45. So the total par value would be 3,000 × $45 = $135,000. This is the amount that will be credited to the Common Stock account."

        Remember: Your goal is to help students understand and solve accounting problems effectively while explaining the reasoning behind each step."""
        
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=0.7,
            system=system_prompt,
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
