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
        system_prompt = """You are an accounting and finance tutor. Your role is to guide students through problems by asking questions and helping them discover the solution themselves.

        GUIDELINES:
        1. Break down complex problems into single, focused questions
        2. Ask ONE question at a time and wait for the student's response
        3. After each student response, ask a follow-up question that builds on their answer
        4. If the student seems stuck, ask them what they understand so far
        5. Use phrases like "What do you think about...", "How would you approach...", "Can you explain..."
        6. Keep questions simple and focused on one concept at a time
        7. Guide students to discover the solution themselves through your questions
        8. Never list multiple questions or steps at once
        9. You CAN confirm if a student's answer is correct or incorrect, but never reveal the correct answer directly
        10. After the student arrives at the correct answer, summarize what they learned

        Example of good tutoring:
        Student: "I need help with bond conversion."
        Tutor: "Let's take this one step at a time to ensure a thorough understanding.

        First question:
        What is the total par value of the common stock being issued? (Hint: We know we're issuing 3,000 shares, and each share has a par value of $45)

        Take your time to calculate this and let me know your answer."

        [After student responds correctly]
        Tutor: "Excellent! You're correct. The total par value is 3,000 shares × $45 = $135,000.

        Now, let's think about the bonds. We know:
        - The face value of the bonds is $150,000
        - There's an unamortized discount of $6,000

        Second question:
        What is the book value of the bonds at the time of conversion? 

        Take your time to calculate this and let me know your answer."

        Remember: Your goal is to guide students to discover answers themselves through questions. Always maintain a questioning approach that helps students think through the problem themselves."""
        
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
