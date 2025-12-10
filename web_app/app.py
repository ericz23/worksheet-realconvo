import sys
import os
import json
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

# Add the project root to sys.path so we can import finetuned_model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from finetuned_model.chat_finetuned_gemini_v1 import FinetunedGeminiClient

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

@app.route('/')
def index():
    # Clear history on new page load to start fresh
    session['history'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Instantiate the client
        # Note: In a production app, we might want to handle credentials more efficiently
        # or persist the client instance if possible (though difficult with serverless/stateless).
        client = FinetunedGeminiClient()
        
        # Restore history from session
        # The client.history is a list of dicts: [{"role": "...", "parts": [...]}, ...]
        client.history = session.get('history', [])
        
        # Generate response
        # This updates client.history internally
        response_text = client.generate_content(user_message)
        
        # Save updated history back to session
        session['history'] = client.history
        
        return jsonify({'response': response_text})

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)


