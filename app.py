import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة ومن الماء حياة 2", page_icon="💧", layout="wide")

# 2. دالة الاتصال بالشيت (مع تنظيف المفتاح)
def get_worksheet(sheet_name):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_info = st.secrets["gcp_service_account"]
        
        # تصليح المفتاح السري أوتوماتيكياً
        if "private_key" in creds_info:
            fixed_key = creds_info["private_key"].replace("\\n", "\n").strip()
            clean_creds = {k: v for k, v in creds_info.items()}
            clean_creds["private_key"] = fixed_key
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(clean_creds, scope)
        client = gspread.authorize(creds)
        
        # فتح ملف الإكسيل (تأكد من مطابقة الاسم بالملي)
        sh = client.open("بيانات مشروع الماء حياة 2")
        return sh.worksheet(sheet_name)
    except Exception as e:
        st.error(f"خطأ فني في الاتصال بتابة [{sheet_name}]: {e}")
        return None

# 3. واجهة المستخدم الجانبية (الاختيارات الأساسية)
st.title("💧 منظومة إدارة المشاريع الفنية - ومن الماء حياة")
st.markdown("---")

with st.sidebar:
    st.header("👤 بيانات المحرر")
    employee = st.selectbox("اختر اسم الموظف", ["حسنين منصور", "احمد سنباطي", "فارس جمال", "محمد سامح"])
    project_type = st.selectbox("نوع المشروع", ["محطات تحليه", "ابار شاطئية", "خطوط مياة", "وصلات مياه"])
    
    # تحديد النشاط بناءً على نوع المشروع
    if project_type == "محطات تحليه":
        activity = st.radio("النشاط الحالي", ["استكشاف", "رفع سجل متابعه"])
    elif project_type == "وصلات مياه":
        activity = st.radio("النشاط الحالي", ["استكشاف", "تنفيذ تسكين"])
    else:
        activity = st.radio("النشاط الحالي", ["استكشاف", "تنفيذ"])

st.subheader(f"📋 نموذج: {project_type} - {activity}")

# 4. بناء النموذج (Form)
with st.form("main_report_form"):
    # سنقوم بتخزين كل البيانات في قاموس واحد لضمان عدم حدوث NameError
    d = {} 
    
    # --- قسم الاستكشاف (عام لكل المشاريع) ---
    if activity == "استكشاف":
        c1, c2 = st.columns(2)
        with c1:
            d['المحافظة'] = st.selectbox("المحافظة", ["قنا", "المنيا", "الشرقية", "أخرى"])
            d['المركز'] = st.text_input("المركز")
            d['القرية'] = st.text_input("القرية")
            d['تعداد_السكان'] = st.number_input("تعداد السكان", min_value=0)
        with c2:
            d['حالة_الغرفة'] = st.radio("جاهزية الغرفة", ["جاهزة", "غير جاهزة (محتاجة صيانة)", "لا توجد غرفة"])
            d['أملاح_المياه'] = st.number_input("أملاح مياه القرية (PPM)", min_value=0)
            d['الجهة_المسؤولة'] = st.text_input("الجمعية / الأفراد المسؤولين")
            d['رقم_الهاتف'] = st.text_input("رقم التليفون للتواصل")
        
        d['اللوكيشن'] = st.text_input("لينك اللوكيشن (Google Maps)")
