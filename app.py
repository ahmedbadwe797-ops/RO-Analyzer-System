import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة ومن الماء حياة 2", page_icon="💧", layout="wide")

# 👤 إدارة حالة الدخول والترحيب (Session State) لضمان عدم تكرار ظهور الباب أثناء التنقل
if "door_opened" not in st.session_state:
    st.session_state.door_opened = False

# 🎨 2. حقن الـ CSS المخصص لتغيير لون الخلفية للأزرق وتصميم الباب التفاعلي
st.markdown("""
    <style>
        /* تغيير خلفية التطبيق بالكامل إلى اللون الأزرق المريح */
        .stApp {
            background-color: #EBF5FB !important; /* درجة أزرق سماوي هادئ ونظيف */
        }
        
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
        
        /* تحسين مظهر خلفية حقول الإدخال لتكون بيضاء ومميزة عن الخلفية الزرقاء */
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #FFFFFF !important;
            border: 1px solid #BDC3C7 !important;
            border-radius: 6px !important;
        }
        
        /* ستايل الشاشة الترحيبية والباب */
        .welcome-container {
            text-align: center;
            padding: 50px;
            margin-top: 50px;
            background-color: #2471A3; /* خلفية زرقاء داكنة لكرت الترحيب */
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.15);
            color: white;
        }
        .welcome-title {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
            font-family: 'Arial', sans-serif;
        }
        
        /* ستايل زر الباب الكبير التفاعلي */
        .door-button-style > button {
            background-color: #D35400 !important; /* لون خشبي للباب */
            color: white !important;
            font-size: 50px !important; /* حجم الإيموجي كبير */
            padding: 20px 40px !important;
            border-radius: 12px !important;
            border: 4px solid #A04000 !important;
            cursor: pointer;
            transition: transform 0.5s ease, background-color 0.3s;
        }
        .door-button-style > button:hover {
            transform: scale(1.1) rotate(-5deg); /* تأثير ميلان الباب عند التمرير كأنه يفتح */
            background-color: #E67E22 !important;
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
            clean_cre