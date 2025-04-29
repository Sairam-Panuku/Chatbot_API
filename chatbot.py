from flask import Flask, request, jsonify
import random
import json
import re

app = Flask(__name__)

# Load intents
with open('intents.json') as file:
    intents = json.load(file)

# Simple text matching logic
def get_response(user_input):
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if re.search(r'\b' + re.escape(pattern.lower()) + r'\b', user_input.lower()):
                return random.choice(intent['responses'])
    return "I'm not sure how to respond to that yet."

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run()
