from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import time
import requests
import random

API_KEY = "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"

def get_ai_reply(text):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": text}]}
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return r.json()['choices'][0]['message']['content']
    except: return "AI Error"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# --- تفعيل نظام التخفي (Stealth) بمواصفات iPhone 14 Pro ---
stealth(driver,
    user_agent= "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    languages=["ar-DZ", "ar", "en-US", "en"],
    vendor="Apple Computer, Inc.",
    platform="iPhone",
    webgl_vendor="Apple Inc.",
    renderer="Apple GPU",
    fix_hairline=True,
)

cookies = [
    {'name': 'datr', 'value': 'djlYaSWDVXfRAaW4HwDnRzJC'},
    {'name': 'sb', 'value': 'djlYaY9VCkdqBEUGOLihycfc'},
    {'name': 'c_user', 'value': '61583389620613'},
    {'name': 'xs', 'value': '46:Nt3_BIQ-BFtnTA:2:1767389625:-1:-1'},
    {'name': 'fr', 'value': '0J9fq3YSiqTzy4W1C.AWe0mfjubjlGoGxNUjzxGYjHQ1eEQlxWZn0RpizM_e6t_jk9mxs.BpWDl2..AAA.0.0.BpWDnB.AWfNEWXdC3yKlH20IGtB1PYHzSQ'}
]

def start_bot():
    print("🕵️ تفعيل بصمة iPhone 14 Pro المتقدمة...")
    try:
        driver.get("https://m.facebook.com")
        time.sleep(random.uniform(2, 5))
        
        for cookie in cookies:
            driver.add_cookie(cookie)
        
        driver.refresh()
        time.sleep(random.uniform(5, 8))
        
        if "c_user" in driver.page_source:
            print("✅ الدخول ناجح: البصمة مطابقة للجهاز الحقيقي.")
        else:
            print("❌ فشل الدخول: قد تحتاج لتحديث الكوكيز.")
            return

        while True:
            # محاكاة سلوك بشري: لا يفتح الصفحة كل ثانية بل بشكل عشوائي
            driver.get("https://mbasic.facebook.com/messages/?unread=1")
            print(f"👁️ فحص الرسائل في: {time.strftime('%H:%M:%S')}")
            
            # تأخير عشوائي طويل قليلاً لتجنب كشف السيرفر
            time.sleep(random.randint(45, 90))
            
    except Exception as e:
        print(f"⚠️ خطأ: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_bot()
