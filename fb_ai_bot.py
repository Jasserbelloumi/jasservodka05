from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
chrome_options.add_argument("--headless")  # تشغيل بدون واجهة رسومية (ضروري للسيرفر)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled") # لإخفاء أن المتصفح آلي

# محاكاة iPhone 14 Pro
user_agent = "Mozilla/5.0 (iPhone15,3; U; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f"user-agent={user_agent}")

# تشغيل المتصفح
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# الكوكيز الخاصة بك
cookies = [
    {'name': 'datr', 'value': 'djlYaSWDVXfRAaW4HwDnRzJC'},
    {'name': 'sb', 'value': 'djlYaY9VCkdqBEUGOLihycfc'},
    {'name': 'c_user', 'value': '61583389620613'},
    {'name': 'xs', 'value': '46:Nt3_BIQ-BFtnTA:2:1767389625:-1:-1'},
    {'name': 'fr', 'value': '0J9fq3YSiqTzy4W1C.AWe0mfjubjlGoGxNUjzxGYjHQ1eEQlxWZn0RpizM_e6t_jk9mxs.BpWDl2..AAA.0.0.BpWDnB.AWfNEWXdC3yKlH20IGtB1PYHzSQ'}
]

def start_bot():
    print("🚀 جاري البدء بمحاكاة iPhone 14 Pro على سيرفر GitHub...")
    try:
        driver.get("https://m.facebook.com")
        time.sleep(3)
        
        # إضافة الكوكيز
        for cookie in cookies:
            driver.add_cookie(cookie)
        
        driver.refresh()
        time.sleep(5)
        
        if "c_user" in driver.page_source or "61583389620613" in driver.page_source:
            print("✅ تم تسجيل الدخول بنجاح عبر Selenium!")
        else:
            print("❌ فشل تسجيل الدخول. قد تحتاج لكوكيز جديدة أو موافقة من الحساب.")
            # طباعة جزء من محتوى الصفحة لمعرفة الخطأ (Checkpoint مثلاً)
            return

        print("📡 البوت يراقب الرسائل الآن (mbasic)...")
        while True:
            driver.get("https://mbasic.facebook.com/messages/?unread=1")
            time.sleep(10)
            
            # هنا يمكنك إضافة كود البحث عن الرسائل والرد عليها
            # Selenium سيقوم بفتح كل رسالة وكتابة الرد كأنك شخص حقيقي
            print("👁️ يتم فحص البريد الوارد...")
            time.sleep(60) 
            
    except Exception as e:
        print(f"⚠️ حدث خطأ: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_bot()
