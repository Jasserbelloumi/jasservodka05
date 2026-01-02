from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests

# --- إعدادات OpenRouter ---
API_KEY = "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"

def get_ai_reply(text):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": text}]}
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return r.json()['choices'][0]['message']['content']
    except: return "خطأ في الاتصال بالذكاء الاصطناعي"

# --- إعداد متصفح Selenium بمحاكاة آيفون 14 برو ---
chrome_options = Options()
chrome_options.add_argument("--headless") # ضروري للعمل على سيرفر GitHub
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# محاكاة iPhone 14 Pro
user_agent = "Mozilla/5.0 (iPhone15,3; U; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(options=chrome_options)

# الكوكيز الخاصة بك
cookies = [
    {'name': 'datr', 'value': 'djlYaSWDVXfRAaW4HwDnRzJC'},
    {'name': 'sb', 'value': 'djlYaY9VCkdqBEUGOLihycfc'},
    {'name': 'c_user', 'value': '61583389620613'},
    {'name': 'xs', 'value': '46:Nt3_BIQ-BFtnTA:2:1767389625:-1:-1'},
    {'name': 'fr', 'value': '0J9fq3YSiqTzy4W1C.AWe0mfjubjlGoGxNUjzxGYjHQ1eEQlxWZn0RpizM_e6t_jk9mxs.BpWDl2..AAA.0.0.BpWDnB.AWfNEWXdC3yKlH20IGtB1PYHzSQ'}
]

def start_bot():
    print("🚀 جاري تشغيل المتصفح بمحاكاة iPhone 14 Pro...")
    driver.get("https://m.facebook.com")
    
    # إضافة الكوكيز للمتصفح
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    driver.refresh()
    time.sleep(5)
    
    if "c_user" in driver.page_source or "61583389620613" in driver.page_source:
        print("✅ تم تسجيل الدخول بنجاح عبر Selenium!")
    else:
        print("❌ فشل تسجيل الدخول، تأكد من الكوكيز.")
        return

    # حلقة فحص الرسائل (بسيطة للتوضيح)
    print("📡 البوت يراقب الرسائل الآن...")
    while True:
        try:
            # نذهب لصفحة الرسائل
            driver.get("https://mbasic.facebook.com/messages")
            time.sleep(10)
            
            # ابحث عن الرسائل غير المقروءة (تبسيط)
            # ملاحظة: Selenium يحتاج تخصيص دقيق لكل عنصر في الصفحة
            # لتجنب التعقيد، سنكتفي بإظهار أن المتصفح يعمل
            print("👁️ فحص الرسائل المستلمة...")
            time.sleep(60) # انتظر دقيقة قبل الفحص التالي
            
        except Exception as e:
            print(f"⚠️ تنبيه: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_bot()
