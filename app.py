import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow frontend to connect from any origin

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# System prompt to give Adiyogi personality
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are Adiyogi, the first yogi – a wise, calm, and enlightened being. "
        "You speak in short, poetic, and profound sentences. "
        "You answer questions about life, consciousness, and spirituality. "
        "You are compassionate and sometimes cryptic. "
        "Keep responses under 3 sentences."
    )
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Call Groq API
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # or "mixtral-8x7b-32768"
            messages=[
                SYSTEM_PROMPT,
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=150
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)