import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="منظومة إدارة المشروعات - ومن الماء حياة", page_icon="💧", layout="wide")

# دالة الربط (نفس اللي اشتغلت معاك بنجاح)
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_info = st.secrets["gcp_service_account"]
    
    if "private_key" in creds_info:
        fixed_key = creds_info["private_key"].replace("\\n", "\n").strip()
        clean_creds = {k: v for k, v in creds_info.items()}
        clean_creds["private_key"] = fixed_key

    creds = ServiceAccountCredentials.from_json_keyfile_dict(clean_creds, scope)
    client = gspread.authorize(creds)
    # تأكد من اسم الشيت
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

st.title("📑 منظومة التقارير الفنية المتكاملة")
st.markdown("---")

# تقسيم الاستبيان لتبويبات منظمة
tab1, tab2, tab3, tab4 = st.tabs(["📍 البيانات العامة", "⚙️ المواصفات الفنية", "📦 المعدات والقطع", "📸 الوسائط والصور"])

with tab1:
    st.subheader("البيانات الأساسية للموقع")
    col1, col2 = st.columns(2)
    with col1:
        station_name = st.text_input("اسم المحطة / المشروع")
        governorate = st.selectbox("المحافظة", ["قنا", "المنيا", "الشرقية", "أخرى"])
    with col2:
        village = st.text_input("القرية / المركز")
        report_date = st.date_input("تاريخ التقرير", datetime.now())
    
    project_type = st.selectbox("نوع المشروع", ["ترشيح ضفاف الأنهار (RBF)", "محطة تحلية (RO)", "طاقة شمسية", "حفر آبار"])

with tab2:
    st.subheader("التفاصيل الهندسية والفنية")
    if project_type == "ترشيح ضفاف الأنهار (RBF)" or project_type == "حفر آبار":
        col1, col2 = st.columns(2)
        with col1:
            well_depth = st.number_input("إجمالي عمق البئر (متر)", min_value=0.0)
            pump_depth = st.number_input("عمق وضع الطلمبة (متر)", min_value=0.0)
        with col2:
            soil_layers = st.text_area("وصف طبقات التربة")
            static_water_level = st.number_input("مستوى الماء الاستاتيكي (متر)", min_value=0.0)

    elif project_type == "محطة تحلية (RO)":
        col1, col2 = st.columns(2)
        with col1:
            feed_water_ppm = st.number_input("ملوحة المياه الداخلة (PPM)", min_value=0)
            operating_pressure = st.number_input("ضغط التشغيل (Bar)", min_value=0.0)
        with col2:
            production_capacity = st.number_input("الطاقة الإنتاجية (م3/يوم)", min_value=0)

    elif project_type == "طاقة شمسية":
        col1, col2 = st.columns(2)
        with col1:
            panel_count = st.number_input("عدد الألواح", min_value=0)
            inverter_capacity = st.number_input("قدرة الإنفيرتر (كيلو وات)", min_value=0.0)
        with col2:
            structure_type = st.selectbox("نوع الهيكل", ["ثابت", "متحرك"])

with tab3:
    st.subheader("بيان المهمات والمعدات (BOM)")
    bom_details = st.text_area("أدخل قائمة المعدات المستخدمة (النوع، العدد، الملاحظات)")
    technical_notes = st.text_area("ملاحظات فنية إضافية من الموقع")

with tab4:
    st.subheader("التوثيق الصوري")
    st.info("ملاحظة: الصور سيتم تسجيل أسمائها في الشيت. لرفع الصور الفعلي يفضل ربطها بـ Google Drive")
    station_photo = st.file_uploader("رفع صورة المحطة العامة", type=['jpg', 'png', 'jpeg'])
    parts_photo = st.file_uploader("رفع صورة لوحة التحكم / الطلمبات", type=['jpg', 'png', 'jpeg'])

st.markdown("---")
if st.button("إرسال التقرير النهائي واعتماده 🚀"):
    if station_name and village:
        try:
            sh = connect_to_sheet()
            # تجهيز البيانات كصف واحد للحفظ
            data_row = [
                str(report_date), station_name, governorate, village, project_type,
                str(well_depth if 'well_depth' in locals() else ""),
                str(pump_depth if 'pump_depth' in locals() else ""),
                bom_details, technical_notes,
                "تم الرفع" if station_photo else "لا يوجد"
            ]
            sh.append_row(data_row)
            st.balloons()
            st.success("تم حفظ التقرير الفني بنجاح في قاعدة البيانات!")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الحفظ: {e}")
    else:
        st.warning("برجاء ملء البيانات الأساسية (اسم المحطة والقرية) على الأقل.")