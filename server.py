import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")


if not api_key:
    raise ValueError("❌ ERROR: OPENAI_API_KEY is not set! Check your environment variables.")


client = openai.OpenAI(api_key=api_key)


app = Flask(__name__)

def get_openai_response(user_prompt):
    """Function to get response from OpenAI API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    """API Endpoint to handle chat requests"""
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = get_openai_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
