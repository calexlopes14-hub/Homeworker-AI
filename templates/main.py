import os
from flask import Flask, request, jsonify, render_template_string
from google import genai
from google.genai import types

# ============================
# CONFIGURATION
# ============================

# Automatically loads your API key from Render Environment Variables safely
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

client = genai.Client(api_key='AQ.Ab8RN6J4EptP0u7ior-GjgGoQAOBMUhV7cfXj86DyXlSK0w4_g')

app = Flask(__name__)

# ============================
# HTML + CSS + JAVASCRIPT
# ============================

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Homework Helper AI</title>
    <style>
        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family:Arial,Helvetica,sans-serif;
        }
        body{
            background:#0f172a;
            color:white;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
        }
        .container{
            width:90%;
            max-width:900px;
            height:90vh;
            background:#1e293b;
            border-radius:15px;
            overflow:hidden;
            display:flex;
            flex-direction:column;
            box-shadow:0 0 30px rgba(0,0,0,.4);
        }
        header{
            background:#2563eb;
            padding:20px;
            font-size:28px;
            font-weight:bold;
            text-align:center;
        }
        #chat{
            flex:1;
            padding:20px;
            overflow-y:auto;
        }
        .message{
            margin-bottom:15px;
            padding:15px;
            border-radius:10px;
            line-height:1.6;
        }
        .user{
            background:#2563eb;
        }
        .ai{
            background:#334155;
        }
        .input-area{
            display:flex;
            padding:15px;
            background:#0f172a;
        }
        input{
            flex:1;
            padding:15px;
            font-size:16px;
            border:none;
            outline:none;
            border-radius:8px;
        }
        button{
            margin-left:10px;
            padding:15px 25px;
            border:none;
            border-radius:8px;
            background:#22c55e;
            color:white;
            font-size:16px;
            cursor:pointer;
        }
        button:hover{
            background:#16a34a;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            📚 Homework Helper AI
        </header>
        <div id="chat">
            <div class="message ai">
                Hello 👋<br><br>
                I'm your Homework Helper AI.
                Ask me anything!
            </div>
        </div>
        <div class="input-area">
            <input id="question" placeholder="Ask your homework question..." onkeydown="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        async function sendMessage(){
            let input = document.getElementById("question");
            let text = input.value.trim();
            if(text === "") return;

            let chat = document.getElementById("chat");
            chat.innerHTML += `<div class="message user">${text}</div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            let response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: text
                })
            });
            let data = await response.json();

            chat.innerHTML += `<div class="message ai">${data.reply}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""


# ============================
# ROUTES
# ============================

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data["message"]

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
            config=types.GenerateContentConfig(
                temperature=0.7,
                system_instruction="""
You are Homework Helper AI.
Explain clearly.
Be friendly.
Use simple English.
Give examples.
Solve maths step by step.
Answer according to the student's level.
"""
            )
        )
        return jsonify({
            "reply": response.text
        })
    except Exception as e:
        return jsonify({
            "reply": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)
