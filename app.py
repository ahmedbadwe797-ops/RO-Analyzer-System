import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import re

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # 1. قراءة النص الخام من الخزنة
    raw_json = st.secrets["gcp_service_account"]["json_creds"]
    creds_info = json.loads(raw_json)
    
    # 2. تنظيف المفتاح السري (الجزء الحساس)
    if "private_key" in creds_info:
        key = creds_info["private_key"]
        # مسح أي مسافات أو سطور في بداية ونهاية المفتاح
        key = key.strip()
        # تصليح السطور (التحويل من \n لنص حقيقي) لو لزم الأمر
        key = key.replace("\\n", "\n")
        creds_info["private_key"] = key

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

st.title("💧 منظومة الماء حياة - الإصدار النهائي")

# خانات إدخال البيانات
name = st.text_input("اسم المحطة")
village = st.text_input("القرية")

if st.button("اعتماد وحفظ البيانات 💾"):
    if name and village:
        try:
            sh = connect_to_sheet()
            sh.append_row([name, village])
            st.balloons()
            st.success(f"تم الحفظ بنجاح! مبروك يا م. أحمد.")
        except Exception as e:
            # رسالة واضحة للمساعدة في التشخيص لو حصل حاجة
            st.error(f"حدث خطأ فني: {e}")
    else:
        st.warning("يرجى ملء الخانات أولاً")