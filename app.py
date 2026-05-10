import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    try:
        # سحب البيانات كقاموس
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # أهم سطر في الكود: تحويل الـ \n لنص حقيقي عشان جوجل تقبله
        if "private_key" in creds_dict:
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
        return sheet
    except Exception as e:
        st.error(f"فشل الاتصال الفني: {e}")
        return None

# واجهة بسيطة جداً للتأكد
st.title("💧 تجربة الربط النهائية")
name = st.text_input("اسم المحطة للتجربة")

if st.button("حفظ الآن"):
    sh = connect_to_sheet()
    if sh:
        sh.append_row([name, "تجربة نهائية"])
        st.balloons()
        st.success("أخيراً! السيستم نطق واشتغل يا هندسة")