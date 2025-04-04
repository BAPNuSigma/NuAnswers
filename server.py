import os
import anthropic
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Anthropic API key
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: ANTHROPIC_API_KEY is not set! Check your environment variables.")

# Initialize Claude client
client = anthropic.Anthropic(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)

def get_claude_response(user_prompt):
    """Function to get response from Claude API using the Messages API."""
    try:
        print("⚡ Sending request to Claude...")
        print(f"📨 Prompt: {user_prompt}")
        # Using a system message helps define the conversation context
        response = client.messages.create(
            model="claude-3.5-sonnet-20241022",  # Change to "claude-3-5-haiku-20241022" if preferred
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {"role": "system", "content": "You are a helpful tutor bot."},
                {"role": "user", "content": user_prompt}
            ]
        )
        print("✅ Received response from Claude")
        print("📄 Full response:", response)
        return response.content[0].text
    except Exception as e:
        print(f"❌ Error while calling Claude: {str(e)}")
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    """API Endpoint to handle chat requests."""
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response_text = get_claude_response(user_input)
    return jsonify({"response": response_text})

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
