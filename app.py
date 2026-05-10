import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. إعدادات الصفحة والسمات
st.set_page_config(page_title="منظومة ومن الماء حياة 2", page_icon="💧", layout="wide")

# 2. دالة الاتصال الذكي بالشيت
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
        # تأكد من أن اسم الملف هو "بيانات مشروع الماء حياة 2"
        sh = client.open("بيانات مشروع الماء حياة 2")
        return sh.worksheet(sheet_name)
    except Exception as e:
        st.error(f"خطأ في الوصول للتابة {sheet_name}: {e}")
        return None

# 3. واجهة المستخدم - اختيار الموظف والنشاط
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

# 4. بناء النماذج الديناميكية
st.subheader(f"📋 نموذج: {project_type} - {activity}")

with st.form("main_form"):
    data_to_save = {}
    
    # أ. حالة الاستكشاف (عامة لكل المشاريع)
    if activity == "استكشاف":
        col1, col2 = st.columns(2)
        with col1:
            data_to_save['محافظة'] = st.selectbox("المحافظة", ["قنا", "المنيا", "سوهاج", "اسيوط"])
            data_to_save['مركز'] = st.text_input("المركز")
            data_to_save['قرية'] = st.text_input("القرية")
            data_to_save['تعداد'] = st.number_input("تعداد السكان", min_value=0)
        with col2:
            data_to_save['غرفة'] = st.radio("جاهزية الغرفة", ["جاهزة", "غير جاهزة (محتاجة صيانة)", "لا توجد غرفة"])
            data_to_save['املاح'] = st.number_input("أملاح مياه القرية (PPM)", min_value=0)
            data_to_save['مسؤول'] = st.text_input("الجمعية / الفرد المسؤول")
            data_to_save['هاتف'] = st.text_input("رقم التليفون للتواصل")
        
        data_to_save['لوكيشن'] = st.text_input("لينك اللوكيشن (Google Maps)")
        
        if project_type == "وصلات مياه":
            st.info("تفاصيل إضافية للوصلات")
            data_to_save['عدد_وصلات'] = st.number_input("عدد الوصلات المتوقع", min_value=0)
            data_to_save['حالة_البيت'] = st.selectbox("حالة البيوت", ["متهالكة", "متوسطة", "جيدة"])
            data_to_save['مستوى_الفقر'] = st.select_slider("مستوى الاحتياج", options=["متوسط", "شديد", "معدم"])

    # ب. سجل متابعة المحطات
    elif activity == "رفع سجل متابعه":
        col1, col2 = st.columns(2)
        with col1:
            data_to_save['املاح_دخول'] = st.number_input("الأملاح (دخول)", min_value=0)
            data_to_save['املاح_خروج'] = st.number_input("الأملاح (منتج)", min_value=0)
            data_to_save['ضغط_تشغيل'] = st.number_input("الضغط (Bar)", min_value=0.0)
            data_to_save['مواتير'] = st.selectbox("حالة المواتير", ["ممتازة", "تحتاج صيانة", "عطلانة"])
        with col2:
            data_to_save['فيزلات'] = st.multiselect("حالة الفيزلات", ["رمل", "كربون", "بيرم"], default=["رمل", "كربون", "بيرم"])
            data_to_save['ممبرين'] = st.text_input("حالة الممبرينات (1 إليمنت لكل هاوسنج)")
            data_to_save['نوع_شمع'] = st.selectbox("نوع الشمع المستخدم", ["10 عادي", "10 جامبو", "20 عادي", "20 جامبو"])
            data_to_save['عدد_شمع'] = st.number_input("عدد الشمع الكلي (مفرد)", min_value=0)

    # ج. تنفيذ (خطوط / وصلات)
    elif "تنفيذ" in activity:
        if project_type == "وصلات مياه":
            data_to_save['متبرع'] = st.text_input("اسم المتبرع")
            data_to_save['صورة_بطاقة'] = st.file_uploader("رفع صورة البطاقة", type=['jpg', 'png', 'jpeg'])
        
        data_to_save['مواصفات_تنفيذ'] = st.text_area("تفاصيل التنفيذ (أطوال/مقاسات/أعماق)")
        data_to_save['لوكيشن'] = st.text_input("لينك لوكيشن التنفيذ")

    # خانات عامة
    data_to_save['شكوى'] = st.text_area("هل توجد شكوى؟")
    data_to_save['راي_متابع'] = st.text_area("رأي المتابع الفني")
    station_img = st.file_uploader("رفع صور الموقع / المحطة", type=['jpg', 'png', 'jpeg'])

    submitted = st.form_submit_button("إرسال البيانات واعتماد التقرير ✅")

    if submitted:
        if not village and activity == "استكشاف":
            st.warning("برجاء إدخال اسم القرية")
        else:
            with st.spinner("جاري تصنيف البيانات وحفظها في التابة المخصصة..."):
                # تحديد التابة والصف
                target_tab = ""
                if activity == "استكشاف": target_tab = "Exploration"
                elif activity == "رفع سجل متابعه": target_tab = "Station_Followup"
                elif project_type == "خطوط مياة": target_tab = "Pipeline_Execution"
                else: target_tab = "Connection_Execution"
                
                ws = get_worksheet(target_tab)
                if ws:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # تحويل القاموس لقائمة مرتبة (يجب تنسيق رؤوس الأعمدة في الشيت يدوياً أولاً)
                    row = [timestamp, employee, project_type, activity] + list(data_to_save.values())
                    ws.append_row(row)
                    st.balloons()
                    st.success(f"تم الحفظ في تابة [{target_tab}] بنجاح!")
