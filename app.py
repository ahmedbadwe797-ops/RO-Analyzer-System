import streamlit as st
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- 1. إعدادات الربط بجوجل شيت ---
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    # تأكد أن هذا الاسم هو نفس اسم الشيت في جوجل بالضبط (بيانات مشروع الماء حياة 2)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet

# --- 2. إعدادات الصفحة والهوية ---
st.set_page_config(page_title="مشروع الماء حياة 2 - التقييم الفني", page_icon="💧", layout="wide")

# عرض اللوجو المدمج
col_empty1, col_main_logo, col_empty2 = st.columns([1, 2, 1])
with col_main_logo:
    if os.path.exists("logos.png"):
        st.image("logos.png", use_column_width=True)

st.markdown("<h1 style='text-align: center;'>🚀 منظومة تقييم واختيار محطات (الماء حياة 2)</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>تحت إشراف مدير المكتب الفني: م. أحمد بدوي</h4>", unsafe_allow_html=True)

# --- 3. تقسيم الاستبيان لتبويبات ---
tab1, tab2, tab3, tab4 = st.tabs(["🚫 البيانات الأساسية والاستبعاد", "🛠️ الفحص الفني", "📊 اللوجستيات", "📝 التقرير النهائي"])

# --- التبويب الأول: البيانات التعريفية والفلتر الأولي ---
with tab1:
    st.header("📍 بيانات هوية المحطة والجمعية")
    
    col_id1, col_id2 = st.columns(2)
    with col_id1:
        station_name = st.text_input("اسم المحطة الشائع", placeholder="مثال: محطة مياه الرحمن")
        parent_association = st.text_input("اسم الجمعية التابعة لها", placeholder="الجمعية الشرعية بقرية...")
        governorate = st.selectbox("المحافظة", ["قنا", "المنيا", "أسيوط", "سوهاج", "الأقصر", "أخرى"])
    
    with col_id2:
        markaz = st.text_input("المركز / القسم", placeholder="مثال: مركز قوص")
        village = st.text_input("القرية / المنطقة", placeholder="مثال: قرية حجازة")

    st.markdown("---")
    st.header("🛑 فلتر الجدية (Red Flags)")
    col_check1, col_check2 = st.columns(2)
    with col_check1:
        agree_protocol = st.radio("الموافقة على توقيع البروتوكول؟", ["نعم", "لا"])
        agree_training = st.radio("الالتزام بحضور التدريبات؟", ["نعم", "لا"])
    with col_check2:
        agree_awareness = st.radio("المشاركة في حملات التوعية؟", ["نعم", "لا"])
        provide_technician = st.radio("توفير فني مقيم للمحطة؟", ["نعم", "لا"])
    
    if "لا" in [agree_protocol, agree_training, agree_awareness, provide_technician]:
        st.error("⚠️ المحطة مستبعدة نهائياً لعدم استيفاء شروط التعاون.")
        st.stop()
    else:
        st.success("✅ تم استيفاء الشروط المبدئية.")

# --- التبويب الثاني: الفحص الفني ---
with tab2:
    st.header("⚙️ تفاصيل المعدات")
    m_hp = st.number_input("قدرة الموتور الابتدائي (حصان)", value=1.5)
    vessel_count = st.number_input("عدد الفيزلات", value=3)
    membrane_count = st.number_input("إجمالي عدد الممبرينات", value=1)
    f_tds = st.number_input("ملوحة المغذي (Feed TDS)", value=1000)
    p_tds = st.number_input("ملوحة المنتج (Permeate TDS)", value=50)

# --- التبويب الثالث: اللوجستيات ---
with tab3:
    st.header("📊 الدراسة الديموغرافية")
    population = st.number_input("تعداد سكان القرية", value=15000)
    current_stations = st.number_input("عدد المحطات الحالية بالقرية", value=1)
    gap = (population / 15000) - current_stations
    st.metric("فجوة الاحتياج", f"{gap:.1f} محطة")

# --- التبويب الرابع: حفظ البيانات ---
with tab4:
    st.header("📝 التقييم النهائي")
    inspector_notes = st.text_area("ملاحظات المستكشف الفنية")
    
    if st.button("اعتماد وحفظ التقرير في الشيت 💾"):
        try:
            sheet = connect_to_sheet()
            row = [
                station_name, parent_association, governorate, markaz, village,
                agree_protocol, agree_training, agree_awareness, provide_technician,
                m_hp, vessel_count, membrane_count, f_tds, p_tds,
                population, current_stations, gap, inspector_notes
            ]
            sheet.append_row(row)
            st.balloons()
            st.success(f"تم بنجاح حفظ بيانات محطة {station_name}!")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")