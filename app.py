import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # قراءة النص الخام من الخزنة
    raw_json = st.secrets["gcp_service_account"]["json_data"]
    creds_info = json.loads(raw_json)
    
    # تنظيف المفتاح من أي حروف مختفية أو مسافات زيادة
    if "private_key" in creds_info:
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n").strip()

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

st.title("💧 نظام تسجيل محطات الماء حياة 2")

# خانات التجربة
name = st.text_input("اسم المحطة")
village = st.text_input("القرية")

if st.button("حفظ البيانات 💾"):
    if name and village:
        try:
            sh = connect_to_sheet()
            sh.append_row([name, village])
            st.balloons()
            st.success(f"مبروك يا هندسة! تم تسجيل {name} في الشيت.")
        except Exception as e:
            st.error(f"حدث خطأ في التشفير: {e}")
    else:
        st.warning("يرجى إدخال البيانات أولاً")