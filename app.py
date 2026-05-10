import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# دالة الربط اللي هتنهي المشكلة
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # قراءة المفتاح كـ "نص خام" وتحويله لقاموس (Dictionary)
    try:
        raw_json_str = st.secrets["json_creds"]
        creds_info = json.loads(raw_json_str)
        
        # تصليح يدوي لأي لخبطة في السطور الجديدة داخل المفتاح
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
            
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        client = gspread.authorize(creds)
        
        # تأكد إن ده اسم الشيت عندك بالظبط
        sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
        return sheet
    except Exception as e:
        st.error(f"فشل الاتصال بجوجل شيت: {e}")
        return None

st.title("💧 نظام تسجيل المحطات - الإصدار النهائي")

# خانات بسيطة للتجربة
station = st.text_input("اسم المحطة")
village = st.text_input("القرية")

if st.button("حفظ البيانات الآن 💾"):
    if station and village:
        sh = connect_to_sheet()
        if sh:
            try:
                sh.append_row([station, village])
                st.balloons()
                st.success(f"مبروك يا هندسة! تم تسجيل {station} في الشيت.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء الكتابة: {e}")
    else:
        st.warning("يرجى إدخال اسم المحطة والقرية")