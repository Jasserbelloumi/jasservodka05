import requests
import json
from fbchat import Client
from fbchat.models import Message

# --- إعدادات OpenRouter ---
API_KEY = "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"
AI_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_ai_response(user_text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "FB-AI-Bot"
    }
    data = {
        "model": "openai/gpt-3.5-turbo", 
        "messages": [{"role": "user", "content": user_text}]
    }
    try:
        res = requests.post(AI_URL, headers=headers, json=data)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        else:
            return "عذراً، هناك مشكلة في الاتصال بالذكاء الاصطناعي حالياً."
    except Exception as e:
        return f"خطأ تقني: {str(e)}"

# --- إعدادات بوت فيسبوك ---
class JasserBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if author_id == self.uid:
            return
        msg_text = message_object.text
        if msg_text and msg_text.lower().startswith("/bot"):
            query = msg_text.replace("/bot", "").strip()
            print(f"📥 تم استلام طلب: {query}")
            self.markAsRead(thread_id)
            ai_reply = get_ai_response(query)
            self.send(Message(text=ai_reply), thread_id=thread_id, thread_type=thread_type)
            print("✅ تم إرسال الرد بنجاح.")

# --- تسجيل الدخول بالكوكيز ---
session_cookies = {
    "datr": "djlYaSWDVXfRAaW4HwDnRzJC",
    "sb": "djlYaY9VCkdqBEUGOLihycfc",
    "c_user": "61583389620613",
    "xs": "46:Nt3_BIQ-BFtnTA:2:1767389625:-1:-1",
    "fr": "0J9fq3YSiqTzy4W1C.AWe0mfjubjlGoGxNUjzxGYjHQ1eEQlxWZn0RpizM_e6t_jk9mxs.BpWDl2..AAA.0.0.BpWDnB.AWfNEWXdC3yKlH20IGtB1PYHzSQ"
}

try:
    print("⏳ جاري محاولة الدخول إلى فيسبوك...")
    client = JasserBot("", "", session_cookies=session_cookies)
    print("🚀 البوت متصل الآن!")
    client.listen()
except Exception as e:
    print(f"❌ فشل تسجيل الدخول: {e}")
