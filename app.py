import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# --- 1. دالة الربط بجوجل شيت (باستخدام الخزنة Secrets) ---
def connect_to_sheet():
    # الصلاحيات المطلوبة
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # جلب البيانات من "الخزنة" (Secrets) اللي إنت لسه ماليها في موقع ستريمليت
    creds_info = st.secrets["gcp_service_account"]
    
    # تحويل البيانات لتنسيق يفهمه جوجل
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)
    
    # فتح الشيت (تأكد إن الاسم هو ده بالظبط في جوجل)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

# --- 2. إعدادات واجهة الموقع ---
st.set_page_config(page_title="منظومة الماء حياة 2", page_icon="💧", layout="wide")

# عرض اللوجو (لو رفعت ملف logos.png على جيت هب)
if os.path.exists("logos.png"):
    st.image("logos.png")

st.title("🚀 نظام التقييم الفني للمحطات")
st.markdown("---")

# --- 3. تقسيم الاستبيان لتبويبات (Tabs) ---
tab1, tab2, tab3 = st.tabs(["📍 البيانات الأساسية", "⚙️ الفحص الفني", "📝 التقرير النهائي"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        station_name = st.text_input("اسم المحطة")
        governorate = st.selectbox("المحافظة", ["قنا", "المنيا", "أسيوط", "سوهاج", "الأقصر"])
    with col2:
        markaz = st.text_input("المركز")
        village = st.text_input("القرية")

with tab2:
    f_tds = st.number_input("ملوحة المغذي (Feed TDS)", value=1000)
    p_tds = st.number_input("ملوحة المنتج (Permeate TDS)", value=50)
    notes = st.text_area("ملاحظات الفحص الفني")

with tab3:
    st.subheader("حفظ البيانات")
    if st.button("اعتماد وحفظ في جوجل شيت 💾"):
        try:
            # الاتصال بالشيت
            sheet = connect_to_sheet()
            
            # تجهيز السطر اللي هيتكتب
            data_row = [station_name, governorate, markaz, village, f_tds, p_tds, notes]
            
            # إضافة السطر للشيت
            sheet.append_row(data_row)
            
            st.balloons()
            st.success(f"تم حفظ بيانات {station_name} بنجاح!")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الحفظ: {e}")