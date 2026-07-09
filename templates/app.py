from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

app = Flask(__name__)

client = genai.Client(api_key="YOUR_API_KEY_HERE")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data["message"]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message,
        config=types.GenerateContentConfig(
            temperature=0.7
        )
    )

    return jsonify({"reply": response.text})


if __name__ == "__main__":
    app.run(debug=True)

app = Flask(__name__)

