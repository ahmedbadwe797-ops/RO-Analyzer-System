import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # تحويل الأسرار لـ "قاموس" عادي عشان نقدر نعدل فيه (حل مشكلة item assignment)
    creds_info = dict(st.secrets["gcp_service_account"])
    
    # تصليح شكل المفتاح السري
    if "private_key" in creds_info:
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

st.title("💧 نظام تسجيل المحطات - تجربة")

# الخانات البسيطة اللي جربناها
name = st.text_input("اسم المحطة")
village = st.text_input("القرية")

if st.button("حفظ الآن"):
    try:
        sh = connect_to_sheet()
        sh.append_row([name, village])
        st.balloons()
        st.success("مبروك يا هندسة! السطر نزل في الشيت")
    except Exception as e:
        st.error(f"لسه فيه مشكلة: {e}")