import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # قراءة النص الخام من الخزنة وفكه كـ JSON
    try:
        # بنجيب النص اللي إنت لزقته في الخزنة
        json_string = st.secrets["gcp_service_account"]["full_json"]
        
        # بنحوله لبيانات حقيقية (السطر ده بيحل كل مشاكل التشفير والمسافات)
        creds_info = json.loads(json_string)
        
        # تصليح السطور في المفتاح السري (ضرورية جداً)
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")

        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        client = gspread.authorize(creds)
        
        # افتح الشيت
        sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
        return sheet
    except Exception as e:
        st.error(f"فشل الاتصال: {e}")
        return None

st.title("💧 منظومة الماء حياة - الإصدار النهائي")

name = st.text_input("اسم المحطة")
village = st.text_input("القرية")

if st.button("حفظ البيانات 💾"):
    if name and village:
        sh = connect_to_sheet()
        if sh:
            try:
                sh.append_row([name, village])
                st.balloons()
                st.success("أخيراً! تم الحفظ بنجاح.")
            except Exception as e:
                st.error(f"خطأ في الكتابة: {e}")
    else:
        st.warning("دخل البيانات يا هندسة")