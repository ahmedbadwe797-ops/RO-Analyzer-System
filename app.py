import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# --- 1. دالة الربط الاحترافية (قراءة الملف كامل من الخزنة) ---
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        # قراءة النص الخام من متغير json_creds في Secrets
        raw_json = st.secrets["json_creds"]
        creds_info = json.loads(raw_json)
        
        # تصليح المفتاح السري لو فيه أي لخبطة في التنسيق
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
            
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        client = gspread.authorize(creds)
        
        # افتح الشيت (تأكد إن الاسم ده هو اللي في جوجل بالضبط)
        sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
        return sheet
    except Exception as e:
        st.error(f"فشل الاتصال بالقاعدة: {e}")
        return None

# --- 2. إعدادات الواجهة والهوية ---
st.set_page_config(page_title="منظومة الماء حياة 2", page_icon="💧", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🚀 نظام التقييم الفني للمحطات</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>إشراف المكتب الفني - م. أحمد بدوي</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. تقسيم الاستبيان لتبويبات (Tabs) ---
tab1, tab2, tab3, tab4 = st.tabs(["📍 بيانات الموقع", "⚙️ الفحص الفني", "📊 اللوجستيات", "📝 التقرير النهائي"])

with tab1:
    st.header("بيانات هوية المحطة")
    col1, col2 = st.columns(2)
    with col1:
        station_name = st.text_input("اسم المحطة الشائع")
        parent_association = st.text_input("اسم الجمعية التابعة لها")
        governorate = st.selectbox("المحافظة", ["قنا", "المنيا", "أسيوط", "سوهاج", "الأقصر", "أخرى"])
    with col2:
        markaz = st.text_input("المركز / القسم")
        village = st.text_input("القرية / المنطقة")
    
    st.markdown("---")
    st.subheader("🛑 فلتر الاستبعاد الأولي")
    agree_protocol = st.radio("هل الجمعية موافقة على توقيع البروتوكول؟", ["نعم", "لا"])
    provide_technician = st.radio("هل الجمعية ملتزمة بتوفير فني مقيم؟", ["نعم", "لا"])
    
    if agree_protocol == "لا" or provide_technician == "لا":
        st.warning("⚠️ تنبيه: المحطة قد لا تستوفي الشروط الأساسية للمشروع.")

with tab2:
    st.header("⚙️ الفحص الفني للمعدات")
    col3, col4 = st.columns(2)
    with col3:
        m_hp = st.number_input("قدرة الموتور الحالي (حصان)", value=1.5)
        vessel_count = st.number_input("عدد الفيزلات", value=3)
    with col4:
        f_tds = st.number_input("ملوحة المغذي (Feed TDS)", value=1000)
        p_tds = st.number_input("ملوحة المنتج (Permeate TDS)", value=50)

with tab3:
    st.header("📊 دراسة الاحتياج (اللوجستيات)")
    population = st.number_input("تعداد سكان القرية المستفيدة", value=15000)
    current_stations = st.number_input("عدد المحطات الحالية في نفس القرية", value=1)
    # معادلة بسيطة لحساب الفجوة
    gap = (population / 15000) - current_stations
    st.metric("فجوة الاحتياج التقريبية", f"{gap:.1f} محطة")

with tab4:
    st.header("📝 الملاحظات والاعتماد")
    inspector_notes = st.text_area("ملاحظات المستكشف الفنية والإنشائية")
    
    if st.button("حفظ التقرير بالكامل في الشيت 💾"):
        if station_name and village:
            sh = connect_to_sheet()
            if sh:
                try:
                    # تجميع كل البيانات في سطر واحد مرتب
                    row = [
                        station_name, parent_association, governorate, markaz, village,
                        agree_protocol, provide_technician, m_hp, vessel_count,
                        f_tds, p_tds, population, current_stations, gap, inspector_notes
                    ]
                    sh.append_row(row)
                    st.balloons()
                    st.success(f"تم بنجاح حفظ بيانات محطة {station_name}!")
                except Exception as e:
                    st.error(f"خطأ أثناء الكتابة: {e}")
        else:
            st.error("يرجى العودة لتبويب (بيانات الموقع) وكتابة اسم المحطة والقرية أولاً.")