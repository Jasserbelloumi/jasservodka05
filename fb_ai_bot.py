import sys
import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth

def print_live(text):
    print(text)
    sys.stdout.flush()

# --- البيانات ---
USER_ID = "61583389620613"
PASS_WORD = "jasser vodka"
API_KEY = "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"

def get_ai_reply(text):
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", 
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": text}]},
            timeout=15)
        return r.json()['choices'][0]['message']['content']
    except: return "AI Error"

print_live("⚙️ جاري تجهيز متصفح iPhone 14 Pro...")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# بصمة آيفون 14 برو كاملة
stealth(driver,
    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    languages=["ar-DZ", "ar"],
    vendor="Apple Computer, Inc.",
    platform="iPhone",
    webgl_vendor="Apple Inc.",
    renderer="Apple GPU",
    fix_hairline=True,
)

def login_to_facebook():
    try:
        print_live("🌐 الدخول إلى فيسبوك...")
        driver.get("https://mbasic.facebook.com/login")
        time.sleep(3)
        
        print_live("🔑 إدخال البيانات...")
        driver.find_element(By.NAME, "email").send_keys(USER_ID)
        driver.find_element(By.NAME, "pass").send_keys(PASS_WORD)
        driver.find_element(By.NAME, "login").click()
        
        time.sleep(10) # وقت كافٍ للتحميل
        
        if "c_user" in driver.page_source or "checkpoint" in driver.current_url:
            print_live("✅ تم إرسال طلب الدخول!")
            if "checkpoint" in driver.current_url:
                print_live("⚠️ فيسبوك يطلب تأكيد الهوية. افتح حسابك من الهاتف واضغط 'نعم هذا أنا'.")
            return True
        else:
            print_live("❌ فشل الدخول. قد تكون البيانات خاطئة أو الحساب محمي.")
            return False
    except Exception as e:
        print_live(f"❌ خطأ أثناء تسجيل الدخول: {e}")
        return False

def start_bot():
    if not login_to_facebook(): return

    while True:
        try:
            print_live(f"🔍 فحص الرسائل ({time.strftime('%H:%M:%S')})...")
            driver.get("https://mbasic.facebook.com/messages/?unread=1")
            time.sleep(5)
            
            unread_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/messages/read/')]")
            if unread_links:
                unread_links[0].click()
                time.sleep(3)
                
                messages = driver.find_elements(By.XPATH, "//div/div/div/div")
                if messages:
                    last_text = messages[-1].text
                    print_live(f"💬 رسالة جديدة: {last_text}")
                    
                    if "/bot" in last_text.lower():
                        query = last_text.lower().split("/bot")[-1].strip()
                        reply = get_ai_reply(query)
                        driver.find_element(By.NAME, "body").send_keys(reply)
                        driver.find_element(By.NAME, "Send").click()
                        print_live("✅ تم الرد.")
            
            time.sleep(random.randint(40, 80))
        except Exception as e:
            print_live(f"⚠️ خطأ: {e}")
            time.sleep(30)

if __name__ == "__main__":
    start_bot()
