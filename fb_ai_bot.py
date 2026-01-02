import requests
import json
from fbchat import Client
from fbchat.models import Message

# --- OpenRouter Setup ---
API_KEY = "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"

def get_ai_response(user_text):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "openai/gpt-3.5-turbo", 
        "messages": [{"role": "user", "content": user_text}]
    }
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return res.json()['choices'][0]['message']['content']
    except:
        return "AI Error"

class JasserBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if author_id == self.uid: return
        msg = message_object.text
        if msg and msg.lower().startswith("/bot"):
            query = msg.replace("/bot", "").strip()
            reply = get_ai_response(query)
            self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)

# Cookies dictionary
cookies = {
    "datr": "djlYaSWDVXfRAaW4HwDnRzJC",
    "sb": "djlYaY9VCkdqBEUGOLihycfc",
    "c_user": "61583389620613",
    "xs": "46:Nt3_BIQ-BFtnTA:2:1767389625:-1:-1",
    "fr": "0J9fq3YSiqTzy4W1C.AWe0mfjubjlGoGxNUjzxGYjHQ1eEQlxWZn0RpizM_e6t_jk9mxs.BpWDl2..AAA.0.0.BpWDnB.AWfNEWXdC3yKlH20IGtB1PYHzSQ"
}

try:
    client = JasserBot("", "", session_cookies=cookies)
    print("✅ Bot is online!")
    client.listen()
except Exception as e:
    print(f"❌ Error: {e}")
