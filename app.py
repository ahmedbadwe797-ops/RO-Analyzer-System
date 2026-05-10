import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # قراءة النص الخام من الخزنة وتحويله لبيانات
    raw_json = st.secrets["json_creds"]
    creds_info = json.loads(raw_json)
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

st.title("💧 نظام تسجيل المحطات - تجربة نهائية")

name = st.text_input("اسم المحطة")
village = st.text_input("القرية")

if st.button("حفظ الآن"):
    try:
        sh = connect_to_sheet()
        sh.append_row([name, village])
        st.balloons()
        st.success("مبروك يا هندسة! كدة السيستم اشتغل رسمي والسطر نزل")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")