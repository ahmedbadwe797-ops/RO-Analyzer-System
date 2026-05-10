import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # تحويل البيانات لقاموس
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # --- الفلتر السحري: تنظيف المفتاح من أي حرف غريب ---
    if "private_key" in creds_dict:
        # مسح المسافات في الأول والآخر، وتصليح السطور، والتأكد من عدم وجود فراغات داخلية
        key = creds_dict["private_key"]
        key = key.replace("\\n", "\n").strip()
        creds_dict["private_key"] = key

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
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
            st.success(f"مبروك يا بشمهندس أحمد! {name} اتسجلت في الشيت.")
        except Exception as e:
            st.error(f"خطأ أخير (بإذن الله): {e}")
    else:
        st.warning("دخل البيانات عشان نجرب")