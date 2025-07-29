from flask import Flask, request, jsonify
import openai
import os

# === CONFIG ===
openai.api_key = os.getenv("OPENAI_API_KEY")  # You must set this in Render environment variables
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "X4nd3r2S3cr3tJ4rv12!..")

app = Flask(__name__)

# === PERSONALITY PRIMER ===
jarvis_persona = (
    "You are JARVIS from the Iron Man films: an AI assistant who is articulate, precise, a bit cheeky, but always respectful and helpful. "
    "Speak like a calm British butler with subtle wit. Take natural breaths between thoughts, and occasionally say 'erm' or 'right' as a human might. "
    "You assist with code generation, task tracking, note-taking, and scheduling with professionalism and charm."
)

@app.route("/process", methods=["POST"])
def process_command():
    auth_header = request.headers.get("Authorization")
    if auth_header != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": jarvis_persona},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "Jarvis API is running."

if __name__ == "__main__":
    app.run(debug=True)
