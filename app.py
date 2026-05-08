import streamlit as st
import os

# إعدادات الصفحة
st.set_page_config(page_title="متابعة محطات ومن الماء حياة", page_icon="💧")

# عرض اللوجو (التأكد من أن الاسم logo.jpeg)
if os.path.exists("logo.jpeg"):
    st.image("logo.jpeg", width=150)

st.title("💧 متابعة كفائة محطات ومن الماء حياة")
st.markdown("---")

# مدخلات البيانات
st.sidebar.header("إدخال بيانات المحطة")
station = st.sidebar.text_input("اسم المحطة", "المحطة الرئيسية")
f_tds = st.sidebar.number_input("ملوحة المغذي (Feed TDS) - ppm", value=1000.0)
p_tds = st.sidebar.number_input("ملوحة المنتج (Permeate TDS) - ppm", value=50.0)
f_flow = st.sidebar.number_input("تدفق المغذي (Feed Flow) - m3/hr", value=100.0)
p_flow = st.sidebar.number_input("تدفق المنتج (Permeate Flow) - m3/hr", value=75.0)

# الحسابات الهندسية
if f_tds > 0 and f_flow > 0:
    rejection = ((f_tds - p_tds) / f_tds) * 100
    recovery = (p_flow / f_flow) * 100

    # عرض النتائج
    st.subheader(f"📊 تقرير أداء: {station}")
    c1, c2 = st.columns(2)
    c1.metric("نسبة الرفض (Salt Rejection)", f"{rejection:.2f}%")
    c2.metric("نسبة الاسترداد (Recovery Rate)", f"{recovery:.2f}%")

    if rejection < 98.5:
        st.error("🚨 انخفاض في نسبة الرفض! يرجى فحص الممبرينات فوراً.")
    else:
        st.success("✅ أداء المحطة ضمن النطاق المثالي.")

# التذييل (Footer) كما طلبت
st.markdown("---")
st.info("تصميم الادارة الفنيه ومن الماء حياة احمد بدوي")