import requests
import json
import os
from fbchat import Client
from fbchat.models import Message

# --- إعدادات الذكاء الاصطناعي ---
API_KEY = "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"

def get_ai_response(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "JasserBot"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text}]
    }
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=20)
        return r.json()['choices'][0]['message']['content']
    except:
        return "⚠️ عذراً، لم أستطع معالجة الرد الآن."

# --- كلاس البوت المحسن ---
class JasserBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if author_id == self.uid:
            return

        msg_text = message_object.text
        if msg_text and msg_text.lower().startswith("/bot"):
            query = msg_text.replace("/bot", "").strip()
            print(f"💬 طلب جديد: {query}")
            
            # إرسال رد مؤقت أو جاري الكتابة
            self.markAsRead(thread_id)
            
            response = get_ai_response(query)
            self.send(Message(text=response), thread_id=thread_id, thread_type=thread_type)

# --- الكوكيز الخاصة بك ---
cookies = {
    "datr": "djlYaSWDVXfRAaW4HwDnRzJC",
    "sb": "djlYaY9VCkdqBEUGOLihycfc",
    "c_user": "61583389620613",
    "xs": "46:Nt3_BIQ-BFtnTA:2:1767389625:-1:-1",
    "fr": "0J9fq3YSiqTzy4W1C.AWe0mfjubjlGoGxNUjzxGYjHQ1eEQlxWZn0RpizM_e6t_jk9mxs.BpWDl2..AAA.0.0.BpWDnB.AWfNEWXdC3yKlH20IGtB1PYHzSQ"
}

try:
    # استخدام User Agent ثابت ومعروف لتجنب الحظر
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # محاولة تشغيل البوت
    client = JasserBot("", "", session_cookies=cookies, user_agent=UA)
    print("🚀 تم تشغيل البوت بنجاح! هو الآن جاهز لاستقبال /bot")
    client.listen()
except Exception as e:
    print(f"❌ خطأ في تشغيل البوت: {str(e)}")
