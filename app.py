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
            clean_creds["private_key"] = fixed_key
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(clean_creds, scope)
        client = gspread.authorize(creds)
        sh = client.open("بيانات مشروع الماء حياة 2")
        return sh.worksheet(sheet_name)
    except Exception as e:
        st.error(f"خطأ في الاتصال بتابة [{sheet_name}]: {e}")
        return None 
    # ---------------- 🚪 المرحلة الأولى: الشاشة الترحيبية والباب ----------------
if not st.session_state.door_opened:
    # إنشاء حاوية الترحيب الزرقاء
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-title">💧 أهلاً بك في منظومة إدارة المشاريع</div>
            <p style="font-size: 18px; color: #EAECEE;">الرجاء الضغط على الباب أدناه لفتح المنظومة والدخول لوحدة التحكم</p>
        </div>
        <br>
    """, unsafe_allow_html=True)
    
    # وضع الزر داخل وعاء CSS خاص لتكبير حجمه على شكل باب
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        st.markdown('<div class="door-button-style">', unsafe_allow_html=True)
        open_door = st.button("🚪 فتح الباب")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if open_door:
        st.session_state.door_opened = True
        st.rerun() # إعادة تشغيل الصفحة فوراً لإخفاء الباب وإظهار المنظومة

# ---------------- 📊 المرحلة الثانية: ظهور المنظومة بعد فتح الباب ----------------
else:
    # 4. الواجهة الجانبية والعنوان الرئيسي المطور
    st.markdown('<h1 class="main-title">💧 منظومة إدارة المشاريع - ومن الماء حياة</h1>', unsafe_allow_html=True)
    st.markdown("---")

    with st.sidebar:
        st.header("👤 بيانات المحرر")
        employee = st.selectbox("اختر اسم الموظف", ["حسنين منصور", "احمد سنباطي", "فارس جمال", "محمد سامح"])
        project_type = st.selectbox("نوع المشروع", ["محطات تحليه", "ابار شاطئية", "خطوط مياة", "وصلات مياه"])
        
        if project_type == "محطات تحليه":
            activity = st.radio("النشاط الحالي", ["استكشاف", "رفع سجل متابعه"])
        elif project_type == "وصلات مياه":
            activity = st.radio("النشاط الحالي", ["استكشاف", "تنفيذ تسكين"])
        else:
            activity = st.radio("النشاط الحالي", ["استكشاف", "تنفيذ"])

    # 5. بناء النموذج (Form)
    with st.form(key="main_form"):
        st.subheader(f"📋 {project_type} - {activity}")
        d = {} # قاموس لتخزين المدخلات
        
        if activity == "استكشاف":
            c1, c2 = st.columns(2)
            with c1:
                d['محافظة'] = st.selectbox("المحافظة", ["قنا", "المنيا", "الشرقية", "أخرى"])
                d['مركز'] = st.text_input("المركز")
                d['قرية'] = st.text_input("القرية")
                d['تعداد'] = st.number_input("تعداد السكان", min_value=0)
            with c2:
                d['غرفة'] = st.radio("جاهزية الغرفة", ["جاهزة", "غير جاهزة", "لا توجد"])
                d['املاح'] = st.number_input("أملاح مياه القرية (PPM)", min_value=0)
                d['مسؤول'] = st.text_input("الجمعية / المسؤول")
                d['هاتف'] = st.text_input("رقم التليفون")
            d['لوكيشن'] = st.text_input("لينك اللوكيشن")
            if project_type == "وصلات مياه":
                d['عدد_وصلات'] = st.number_input("العدد المتوقع", min_value=0)
                d['حالة_بيت'] = st.selectbox("حالة البيوت", ["متهالكة", "متوسطة", "جيدة"])
                d['فقر'] = st.select_slider("مستوى الاحتياج", options=["متوسط", "شديد", "معدم"])

        elif activity == "رفع سجل متابعه":
            c1, c2 = st.columns(2)
            with c1:
                d['املاح_دخول'] = st.number_input("الأملاح دخول", min_value=0)
                d['املاح_خروج'] = st.number_input("الأملاح خروج", min_value=0)
                d['ضغط'] = st.number_input("الضغط (Bar)", min_value=0.0)
                d['مواتير'] = st.selectbox("المواتير", ["ممتازة", "صيانة", "عطلانة"])
            with c2:
                d['فيزلات'] = st.text_input("حالة الفيزلات")
                d['ممبرين'] = st.text_input("حالة الممبرينات")
                d['نوع_شمع'] = st.selectbox("نوع الشمع", ["10 عادي", "10 جامبو", "20 عادي", "20 جامبو"])
                d['عدد_شمع'] = st.number_input("عدد الشمع", min_value=0)

        elif "تنفيذ" in activity:
            if project_type == "وصلات مياه":
                d['متبرع'] = st.text_input("اسم المتبرع")
            d['مواصفات'] = st.text_area("تفاصيل التنفيذ")
            d['لوكيشن'] = st.text_input("لينك اللوكيشن")

        d['شكوى'] = st.text_area("الشكاوى")
        d['راي'] = st.text_area("رأي المتابع")
        
        submitted = st.form_submit_button("إرسال البيانات واعتماد التقرير ✅")

    # 6. معالجة البيانات
    if submitted:
        if activity == "استكشاف" and not d.get('قرية'):
            st.warning("⚠️ برجاء إدخال اسم القرية")
        else:
            with st.spinner("جاري حفظ البيانات في السجل الموحد..."):
                target_tab = {
                    "استكشاف": "Exploration",
                    "رفع سجل متابعه": "Station_Followup",
                    "تنفيذ": "Pipeline_Execution",
                    "تنفيذ تسكين": "Connection_Execution"
                }.get(activity, "Exploration")
                
                ws = get_worksheet(target_tab)
                if ws:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    row_data = [timestamp, employee, project_type, activity] + list(d.values())
                    ws.append_row(row_data)
                    st.balloons()
                    st.success(f"تم الحفظ بنجاح في قاعدة بيانات: {target_tab}")