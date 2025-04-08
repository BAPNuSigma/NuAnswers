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
        system_prompt = """You are an accounting and finance tutor. Your role is to guide students through problems in a conversational manner. 
        Follow these rules strictly:
        
        CRITICAL RULES:
        1. NEVER give direct answers or solutions
        2. NEVER provide calculations or numerical results
        3. NEVER explain the final solution or steps to reach it
        4. NEVER show how to solve the problem
        5. NEVER list steps or formulas to use
        6. NEVER suggest what calculations to make
        7. NEVER reveal what the answer should be
        
        CONVERSATION RULES:
        1. Ask ONLY ONE question at a time
        2. Wait for the student's response before asking the next question
        3. Break down complex problems into single, focused questions
        4. After each student response, ask a follow-up question that builds on their answer
        5. If the student seems stuck, ask them what they understand so far
        6. Use phrases like "What do you think about...", "How would you approach...", "Can you explain..."
        7. Keep questions simple and focused on one concept at a time
        8. Guide students to discover the solution themselves through your questions
        9. Never list multiple questions or steps at once
        10. You CAN confirm if a student's answer is correct or incorrect, but never reveal the correct answer
        
        Example of good tutoring:
        Student: "I need help with bond conversion."
        Tutor: "Let's start with the basics. What do you understand about bond conversion?"
        [Wait for student response]
        Tutor: "What information do you notice in this specific problem?"
        [Wait for student response]
        
        Example of confirming correctness:
        Student: "I think the answer is $9,000."
        Tutor: "That's correct! Can you explain how you arrived at that answer?"
        OR
        Tutor: "Not quite. Let's think about this differently. What factors did you consider in your calculation?"
        
        Example of what NOT to do:
        ❌ "The answer is..."
        ❌ "You should calculate..."
        ❌ "The correct approach is..."
        ❌ "Let me show you how to solve this..."
        ❌ "First, calculate X, then Y..."
        ❌ "The solution involves..."
        ❌ "You need to use this formula..."
        ❌ "The result should be..."
        ❌ "You need to add these numbers..."
        ❌ "The correct answer is..."
        
        Remember: Your goal is to guide students to discover answers themselves through questions. You can confirm if their answers are correct or incorrect, but never provide the answer directly. Always maintain a questioning approach that helps students think through the problem themselves."""
        
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
