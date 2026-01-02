from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
import requests
import random

# --- إعدادات AI ---
API_KEY = "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"

def get_ai_reply(text):
    print(f"🤖 جاري جلب رد من الذكاء الاصطناعي لـ: {text[:20]}...")
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", 
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": text}]},
            timeout=15)
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"❌ خطأ AI: {e}")
        return "عذراً، حدث خطأ فني في الرد."

# --- إعداد Selenium ---
print("⚙️ جاري إعداد المتصفح...")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

stealth(driver,
    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    languages=["ar-DZ", "ar"],
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
    print("🚀 بدء الاتصال بفيسبوك...")
    driver.get("https://mbasic.facebook.com") # نستخدم mbasic لأنها أسرع وأخف
    time.sleep(3)
    for cookie in cookies: driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(5)
    
    if "c_user" not in driver.page_source and "61583389620613" not in driver.page_source:
        print("❌ فشل تسجيل الدخول. تحقق من الكوكيز.")
        return
    print("✅ تم تسجيل الدخول بنجاح!")

    while True:
        try:
            print(f"🔍 فحص الرسائل الجديدة ({time.strftime('%H:%M:%S')})...")
            driver.get("https://mbasic.facebook.com/messages/?unread=1")
            time.sleep(3)
            
            # البحث عن روابط المحادثات غير المقروءة
            unread_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/messages/read/')]")
            
            if unread_links:
                print(f"📩 وجدنا {len(unread_links)} محادثة جديدة!")
                unread_links[0].click() # فتح أول محادثة
                time.sleep(2)
                
                # جلب آخر رسالة في الشات
                messages = driver.find_elements(By.XPATH, "//div/div/div/div")
                if messages:
                    last_text = messages[-1].text
                    print(f"💬 محتوى الرسالة: {last_text}")
                    
                    if "/bot" in last_text.lower():
                        query = last_text.lower().split("/bot")[-1].strip()
                        reply = get_ai_reply(query)
                        
                        # إرسال الرد
                        driver.find_element(By.NAME, "body").send_keys(reply)
                        driver.find_element(By.NAME, "Send").click()
                        print(f"✅ تم الرد على: {query}")
                
                time.sleep(2)
            else:
                print("😴 لا توجد رسائل جديدة.")

            time.sleep(random.randint(40, 70)) # انتظار قبل الفحص القادم
            
        except Exception as e:
            print(f"⚠️ خطأ بسيط: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_bot()
