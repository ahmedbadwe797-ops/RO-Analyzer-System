import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# دالة الربط الأبسط والأضمن (بدون تحويل JSON يدوي)
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # قراءة البيانات مباشرة كقاموس (Dictionary) من ستريمليت
    creds_info = st.secrets["gcp_service_account"]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)
    # افتح الشيت (تأكد من الاسم في جوجل)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

st.title("💧 نظام تسجيل محطات الماء حياة 2")

# خانات التجربة
name = st.text_input("اسم المحطة")
village = st.text_input("القرية")

if st.button("حفظ البيانات الآن 💾"):
    if name and village:
        try:
            sh = connect_to_sheet()
            sh.append_row([name, village])
            st.balloons()
            st.success(f"مبروك يا هندسة! تم تسجيل {name} بنجاح.")
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {e}")
    else:
        st.warning("يرجى إدخال البيانات")