import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة ومن الماء حياة 2", page_icon="💧", layout="wide")

# 2. دالة الاتصال بالشيت
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

# 3. الواجهة الجانبية
st.title("💧 منظومة إدارة المشاريع - ومن الماء حياة")
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

# 4. بناء النموذج (Form)
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
    
    # زر الإرسال - يجب أن يكون آخر حاجة جوه الـ with st.form
    submitted = st.form_submit_button("إرسال البيانات واعتماد التقرير ✅")

# 5. معالجة البيانات (خارج الفورم لضمان الاستقرار)
if submitted:
    if activity == "استكشاف" and not d.get('قرية'):
        st.warning("⚠️ برجاء إدخال اسم القرية")
    else:
        with st.spinner("جاري الحفظ..."):
            target_tab = {
                "استكشاف": "Exploration",
                "رفع سجل متابعه": "Station_Followup",
                "تنفيذ": "Pipeline_Execution",
                "تنفيذ تسكين": "Connection_Execution"
            }.get(activity, "Exploration")
            
            ws = get_worksheet(target_tab)
            if ws:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # تجميع الصف بالترتيب: وقت، موظف، مشروع، نشاط، ثم كل المدخلات
                row_data = [timestamp, employee, project_type, activity] + list(d.values())
                ws.append_row(row_data)
                st.balloons()
                st.success(f"تم الحفظ بنجاح في {target_tab}")