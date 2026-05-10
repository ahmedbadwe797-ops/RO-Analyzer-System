import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. دالة الربط - تم تعديلها لتكون "صفر أخطاء"
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # جلب البيانات من الخزنة مباشرة وتحويلها لقاموس
    try:
        creds_info = dict(st.secrets["gcp_service_account"])
        
        # تنظيف المفتاح السري من أي شوائب (حل مشكلة الـ 65 حرف والـ Base64)
        # --- الفلتر النهائي القاطع للأخطاء ---
        if "private_key" in creds_info:
            import re
            key = creds_info["private_key"]
            header = "-----BEGIN PRIVATE KEY-----"
            footer = "-----END PRIVATE KEY-----"
            
            if header in key and footer in key:
                # بناخد اللي بين البداية والنهاية وبنمسح أي حرف مش (حروف، أرقام، +، /، =)
                content = key.split(header)[1].split(footer)[0]
                clean_content = re.sub(r'[^a-zA-Z0-9+/=]', '', content)
                # بنركب المفتاح من جديد نضيف 100%
                creds_info["private_key"] = f"{header}\n{clean_content}\n{footer}"

        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        client = gspread.authorize(creds)
        
        # فتح الشيت (تأكد أن الاسم مطابق تماماً في جوجل درايف)
        sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
        return sheet
    except Exception as e:
        st.error(f"فشل الاتصال: {e}")
        return None

# 2. واجهة المستخدم
st.set_page_config(page_title="منظومة الماء حياة 2", page_icon="💧")
st.title("💧 منظومة الماء حياة - الإصدار النهائي")

name = st.text_input("اسم المحطة")
village = st.text_input("القرية")

if st.button("اعتماد وحفظ البيانات 💾"):
    if name and village:
        with st.spinner('جاري الحفظ...'):
            sh = connect_to_sheet()
            if sh:
                try:
                    sh.append_row([name, village])
                    st.balloons()
                    st.success(f"تم الحفظ بنجاح! مبروك يا م. أحمد.")
                except Exception as e:
                    st.error(f"خطأ أثناء الكتابة في الشيت: {e}")
    else:
        st.warning("يرجى ملء الخانات أولاً")