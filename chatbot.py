from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Import CORS
import random
import json
import re
import requests

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

# Load intents
with open('intents.json') as file:
    intents = json.load(file)

# Intent-based matcher
def intent_response(user_input):
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if re.search(r'\b' + re.escape(pattern.lower()) + r'\b', user_input.lower()):
                return random.choice(intent['responses'])
    return None

# Fallback: Use OpenRouter GPT model
def openrouter_fallback_response(user_input):
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": user_input}]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions", 
        headers=headers, 
        json=data
    )

    try:
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return "Sorry, I couldn't respond right now. Please try again later."

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # First check intent-based response
    response = intent_response(user_input)
    if response:
        return jsonify({"response": response})
    else:
        # If no intent matched, fallback to OpenRouter GPT model
        model_reply = openrouter_fallback_response(user_input)
        return jsonify({"response": model_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
