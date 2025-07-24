import requests
import json
from gtts import gTTS
import os
import time

API_KEY = "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"  # 🔑 यहां अपना OpenRouter API key डालो
MODEL = "openai/gpt-3.5-turbo"  # Bhojpuri समझने के लिए अच्छा model

def ask_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "तू एक Bhojpuri में जवाब देवे वाला chatbot हउ। छोट, साफ़, और सरल भाषा में जवाब दे।"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
    }

    print("🤖 Thinking...")

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload))
        if res.status_code == 200:
            reply = res.json()['choices'][0]['message']['content']
            return reply.strip()
        else:
            return f"❌ Error {res.status_code}: {res.text}"
    except Exception as e:
        return f"⚠️ Failed: {e}"

while True:
    user_input = input("👤 You (Bhojpuri me puchhi): ")
    if user_input.lower() in ['exit', 'quit', 'stop']:
        print("👋 Bye!")
        break

    reply = ask_openrouter(user_input)
    print(f"🤖 Cyber Moranda AI:  {reply}")

    # Speak it
    if not reply.startswith("❌") and not reply.startswith("⚠️"):
        try:
            tts = gTTS(text=reply, lang='hi')
            tts.save("output.mp3")
            os.system("termux-media-player play output.mp3")
        except Exception as e:
            print("❌ Unable to speak:", e)
    else:
        print("❌ Unable to speak.")
