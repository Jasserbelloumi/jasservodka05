import requests
from fbchat import Client
from fbchat.models import Message

# -------- OpenRouter API --------
API_KEY = "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"

def get_ai_response(text):
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "fb-ai-bot"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": text}]
            },
            timeout=30
        )
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return "⚠️ AI غير متاح حالياً"

class AI_Bot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if author_id == self.uid:
            return

        if message_object.text and message_object.text.startswith("/bot"):
            query = message_object.text.replace("/bot", "").strip()
            if not query:
                return
            reply = get_ai_response(query)
            self.send(
                Message(text=reply),
                thread_id=thread_id,
                thread_type=thread_type
            )

# -------- Facebook Cookies Login --------
cookies = {
    "datr": "djlYaSWDVXfRAaW4HwDnRzJC",
    "sb": "djlYaY9VCkdqBEUGOLihycfc",
    "c_user": "61583389620613",
    "xs": "46:Nt3_BIQ-BFtnTA:2:1767389625:-1:-1",
    "fr": "0J9fq3YSiqTzy4W1C.AWe0mfjubjlGoGxNUjzxGYjHQ1eEQlxWZn0RpizM_e6t_jk9mxs.BpWDl2..AAA.0.0.BpWDnB.AWfNEWXdC3yKlH20IGtB1PYHzSQ"
}

try:
    bot = AI_Bot("", "", session_cookies=cookies)
    print("✅ BOT STARTED SUCCESSFULLY")
    bot.listen()
except Exception as e:
    print("❌ LOGIN FAILED:", e)
