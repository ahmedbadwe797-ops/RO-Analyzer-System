import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة ومن الماء حياة 2", page_icon="💧", layout="wide")

# 🎨 2. حقن الـ CSS المخصص لتعديل الألوان والمظهر
st.markdown("""
    <style>
        /* تحسين وتلوين العنوان الرئيسي للمنظومة */
        .main-title {
            color: #1A5276; /* أزرق مائي داكن ورسمي */
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            padding-bottom: 5px;
            text-align: right;
        }
        
        /* تعديل شكل العناوين الفرعية داخل النماذج */
        .stSubheader h3 {
            color: #2E86C1 !important; /* أزرق مائي حيوي */
            font-weight: bold !important;
        }
        
        /* تصميم مخصص واحترافي لزر الإرسال والاعتماد */
        div.stButton > button:first-child {
            background-color: #27AE60 !important; /* أخضر مريح ومناسب للاعتماد */
            color: white !important;
            border-radius: 8px !important;
            font-size: 18px !important;
            font-weight: bold !important;
            border: none !important;
            width: 100% !important;
            padding: 12px !important;
            box-shadow: 0px 4px 10px rgba(39, 174, 96, 0.2);
            transition: all 0.3s ease;
        }
        
        /* تأثير حركي عند تمرير الماوس فوق زر الإرسال */
        div.stButton > button:first-child:hover {
            background-color: #2980B9 !important; /* يتحول للأزرق المائي عند التمرير */
            box-shadow: 0px 6px 15px rgba(41, 128, 185, 0.3);
            cursor: pointer;
        }
        
        /* تحسين مظهر خلفية حقول الإدخال لتكون مريحة للعين */
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #F8F9FA !important;
            border-radius: 6px !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. دالة الاتصال بالشيت
def get_worksheet(sheet_name):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_info = st.secrets["gcp_service_account"]
        
        if "private_key" in creds_info:
            fixed_key = creds_info["private_key"].replace("\\n", "\n").strip()
            clean_creds = {k: v for k, v in creds_info.items()}
            clean_creds["private_key"] = fixed_key
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(clean_creds, scope)
        client = gspread.authorize(creds)
        sh = client.open("بيانات مشروع الماء حياة 2")
        return sh.worksheet(sheet_name)
    except Exception as e:
        st.error(f"خطأ في الاتصال بتابة [{sheet_name}]: {e}")
        return None

# 4. الواجهة الجانبية والعنوان الرئيسي المطور
st.markdown('<h1 class="main-title">💧 منظومة إدارة المشاريع - ومن الماء حياة</h1>', unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.header("👤 بيانات المحرر")
    employee = st.selectbox("اختر اسم الموظف", ["حسنين منصور", "احمد سنباطي", "فارس جمال", "محمد سامح"])
    project_type = st.selectbox("نوع المشروع", ["محطات تحليه", "ابار شاطئية", "خطوط مياة", "وصلات مياه"])
    
    if project_type == "محطات تحليه":
        activity = st.radio("النشاط الحالي", ["استكشاف", "رفع سجل متابعه"])
    elif project_