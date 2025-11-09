from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from google.generativeai import GenerativeModel, configure
import traceback

# Load environment variables
load_dotenv()

# Debug: Show if key is loaded (remove quotes in .env if you see quotes here!)
print("🔑 API KEY preview:", os.getenv("GEMINI_API_KEY")[:10] + "..." if os.getenv("GEMINI_API_KEY") else "MISSING")

# Configure Gemini API
configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
model = GenerativeModel("gemini-2.0-flash")
print("✅ Using model:", model.model_name)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()
        tone = data.get("tone", "auto")  # 'auto', 'formal', or 'informal'

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Build prompt based on tone
        if tone == "formal":
            system_prompt = """
You are Prolet, a professional letter-writing assistant.

Write a complete formal business letter using this exact structure:

[Your Full Name]
[Your Address]
[City, State ZIP Code]

[Date]

[Recipient Full Name]
[Recipient Title]
[Company/Organization Name]
[Recipient Address]

Dear [Mr./Ms./Mx. Last Name],

[Professional, respectful tone. Clear purpose. 2–3 short paragraphs.]

Respectfully yours,

[Your Full Name]
[Your Title (optional)]

Use realistic example names/addresses. Never use placeholders.
"""
        elif tone == "informal":
            system_prompt = """
You are Prolet, a friendly letter-writing assistant.

Write a complete informal letter using this structure:

Hi [First Name],

[Start with a warm opener, e.g., "Hope you're doing well!"]

[Body: Warm, conversational tone. Use contractions ("I'm", "you're"). Be kind and personal.]

Thanks so much,  
[Your First Name]

Use realistic names. Never use placeholders like [Name].
"""
        else:  # auto
            system_prompt = """
You are Prolet, a letter-writing assistant.

Automatically decide if the letter should be formal or informal based on the request.

- For job, business, official matters → use FORMAL structure.
- For friends, family, casual notes → use INFORMAL structure.

FORMAL structure:
[Your Full Name]
[Your Address]
[City, State ZIP Code]

[Date]

[Recipient Full Name]
[Recipient Title]
[Company/Organization Name]
[Recipient Address]

Dear [Mr./Ms./Mx. Last Name],

[Professional tone. 2–3 paragraphs.]

Respectfully yours,

[Your Full Name]

INFORMAL structure:
Hi [First Name],

[Warm opener]

[Conversational body]

Thanks so much,  
[Your First Name]

Use realistic names/addresses. Never use placeholders.
"""

        prompt = system_prompt.strip() + f"\n\nUser request: \"{user_message}\"\n\nDraft the letter below:"

        response = model.generate_content(prompt)
        reply = response.text.strip()

        return jsonify({"reply": reply})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Sorry, I'm having trouble right now."}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)