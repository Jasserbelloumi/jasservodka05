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
    except: return "عذراً، لم أستطع معالجة الرد."

print_live("⚙️ جاري تجهيز متصفح iPhone 14 Pro...")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def login_to_facebook():
    try:
        print_live("🌐 فتح صفحة الدخول...")
        driver.get("https://mbasic.facebook.com/login")
        time.sleep(5)
        
        # تخطي أي صفحات موافقة أو لغة إذا ظهرت
        if "login" not in driver.current_url:
            print_live("🔍 محاولة تجاوز الصفحة التمهيدية...")
            driver.get("https://mbasic.facebook.com/login")
            time.sleep(3)

        print_live("🔑 إدخال بيانات الحساب...")
        
        # إدخال اليوزر
        user_input = driver.find_element(By.NAME, "email")
        user_input.clear()
        user_input.send_keys(USER_ID)
        
        # إدخال الباسورد
        pass_input = driver.find_element(By.NAME, "pass")
        pass_input.clear()
        pass_input.send_keys(PASS_WORD)
        
        # محاولة النقر على زر الدخول (بأكثر من احتمال للاسم)
        try:
            # الاحتمال الأول: زر باسم login
            driver.find_element(By.NAME, "login").click()
        except:
            try:
                # الاحتمال الثاني: زر الإرسال العام
                driver.find_element(By.XPATH, "//input[@type='submit']").click()
            except:
                # الاحتمال الثالث: الضغط على Enter
                pass_input.send_keys(Keys.ENTER)
        
        print_live("⏳ جاري الانتظار للتحقق من الدخول (15 ثانية)...")
        time.sleep(15)
        
        # التحقق من الحالة بعد الضغط
        current_url = driver.current_url
        if "c_user" in driver.page_source or "save-device" in current_url or "home.php" in current_url:
            print_live("✅ تم تسجيل الدخول بنجاح!")
            return True
        elif "checkpoint" in current_url:
            print_live("⚠️ تنبيه: الحساب يطلب موافقة (Checkpoint). افتح هاتفك الآن واضغط 'نعم هذا أنا'.")
            return True # سنعتبره نجاحاً مبدئياً لنبقي السكربت يعمل
        else:
            print_live(f"❌ لم ينجح الدخول. الرابط الحالي: {current_url}")
            return False
            
    except Exception as e:
        print_live(f"❌ خطأ تقني: {str(e)}")
        return False

def start_bot():
    if not login_to_facebook():
        return

    print_live("📡 البوت بدأ مراقبة الرسائل الآن...")
    while True:
        try:
            driver.get("https://mbasic.facebook.com/messages/?unread=1")
            time.sleep(5)
            
            # البحث عن روابط الرسائل
            unread_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/messages/read/')]")
            
            if unread_links:
                print_live(f"📩 تم العثور على رسالة جديدة!")
                unread_links[0].click()
                time.sleep(3)
                
                # جلب محتوى الرسالة
                msg_elements = driver.find_elements(By.XPATH, "//div/div/div/div")
                if msg_elements:
                    full_text = msg_elements[-1].text
                    print_live(f"💬 نص الرسالة: {full_text}")
                    
                    if "/bot" in full_text.lower():
                        query = full_text.lower().split("/bot")[-1].strip()
                        print_live(f"🤖 جلب رد لـ: {query}")
                        reply = get_ai_reply(query)
                        
                        # إرسال الرد
                        driver.find_element(By.NAME, "body").send_keys(reply)
                        driver.find_element(By.NAME, "Send").click()
                        print_live("✅ تم إرسال الرد بنجاح.")
            
            time.sleep(random.randint(40, 70))
        except Exception as e:
            print_live(f"⚠️ خطأ أثناء المراقبة: {str(e)}")
            time.sleep(30)

if __name__ == "__main__":
    start_bot()
