 import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # سحب البيانات مباشرة من الخزنة (بدون تحويل JSON يدوي)
    creds_info = st.secrets["gcp_service_account"]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

st.title("💧 نظام التقييم الفني - الإصدار التجريبي")

# التبويبات المختصرة للتجربة
tab1, tab2 = st.tabs(["📍 البيانات", "💾 الحفظ"])

with tab1:
    station = st.text_input("اسم المحطة")
    village = st.text_input("القرية")

with tab2:
    if st.button("حفظ البيانات الآن"):
        if station and village:
            try:
                sh = connect_to_sheet()
                sh.append_row([station, village])
                st.balloons()
                st.success(f"مبروك يا م. أحمد! السطر نزل في الشيت.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")
        else:
            st.warning("يرجى إدخال البيانات أولاً")