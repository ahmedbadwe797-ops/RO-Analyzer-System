import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # قراءة البيانات مباشرة من الخزنة كقاموس (Dictionary)
    # ده بيخلينا نتفادى مشاكل الـ JSON خالص
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

st.title("💧 نظام تسجيل المحطات - تجربة أخيرة")

# خانات مختصرة عشان نجرب الربط
name = st.text_input("اسم المحطة")
village = st.text_input("القرية")

if st.button("حفظ الآن"):
    if name and village:
        try:
            sh = connect_to_sheet()
            sh.append_row([name, village])
            st.balloons()
            st.success(f"تم الحفظ! مبروك يا ريس، السطر نزل في الشيت.")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
    else:
        st.warning("دخل البيانات الأول")