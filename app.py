from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

@app.route("/quote", methods=["GET"])
def get_quote():
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "parts": [{"text": "Give me a unique and thought-provoking quote for today different than yesterday something inspiring, not too mainstream, preferably from literature, philosophy, or great thinkers. Avoid repeating old common ones and don't exceed three lines of mobile width."}]
        }]
    }

    response = requests.post(
        f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )

    if response.ok:
        quote = response.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"quote": quote})
    else:
        return jsonify({"error": "Failed to fetch quote"}), 500

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8075)
