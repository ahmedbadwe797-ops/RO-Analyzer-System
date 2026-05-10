import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# دالة الربط المضمونة
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # سحب البيانات من الخزنة كقاموس
    creds_info = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

st.title("💧 نظام تسجيل المحطات - م. أحمد بدوي")

# خانات التجربة
station = st.text_input("اسم المحطة")
village = st.text_input("القرية")

if st.button("حفظ البيانات 💾"):
    if station and village:
        try:
            sh = connect_to_sheet()
            sh.append_row([station, village])
            st.balloons()
            st.success(f"مبروك يا هندسة! تم تسجيل {station} بنجاح.")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
    else:
        st.warning("يرجى إدخال البيانات")