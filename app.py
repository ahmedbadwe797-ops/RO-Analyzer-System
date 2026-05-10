import streamlit as st
import os

# 1. إعدادات الصفحة والهوية الرسمية
st.set_page_config(
    page_title="منظومة تقييم محطات الماء حياة 2", 
    page_icon="💧", 
    layout="wide"
)

# --- منطقة الترويسة (Header) ---
# عرض اللوجو المدمج في المنتصف
col_empty1, col_main_logo, col_empty2 = st.columns([1, 2, 1])
with col_main_logo:
    combined_logo_path = "logos.png" 
    if os.path.exists(combined_logo_path):
        st.image(combined_logo_path, use_container_width=True)

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🚀 منظومة تقييم واختيار محطات (الماء حياة 2)</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #6B7280;'>بالتعاون بين مؤسسة ومن الماء حياة ومؤسسة ساويرس للتنمية الاجتماعية</h4>", unsafe_allow_html=True)
st.markdown("---")
st.info("👨‍💻 تصميم وإشراف الإدارة الفنية: م. أحمد بدوي")

# 2. تقسيم الاستبيان لتبويبات (Tabs) لتنظيم العمل الميداني
tab1, tab2, tab3, tab4 = st.tabs([
    "🚫 مرحلة الاستبعاد", 
    "🛠️ الفحص الفني العميق", 
    "📊 الديموغرافيا واللوجستيات", 
    "📝 ملخص رأي المستكشف"
])

# --- التبويب الأول: فحص الاستبعاد (The Knockout Phase) ---
with tab1:
    st.header("🔍 فلاتر القبول والرفض الفورية")
    st.warning("ملحوظة: الإجابة بـ 'لا' على أي سؤال أدناه تعني استبعاد المحطة تلقائياً.")
    
    col1, col2 = st.columns(2)
    with col1:
        q1 = st.radio("1. هل الجمعية موافقة على توقيع بروتوكول تعاون ملزم؟", ["نعم", "لا"], index=1)
        q2 = st.radio("2. هل يلتزم مجلس الإدارة بحضور فنيين للتدريبات؟", ["نعم", "لا"], index=1)
    with col2:
        q3 = st.radio("3. هل توافق الجمعية على استضافة حملات التوعية؟", ["نعم", "لا"], index=1)
        q4 = st.radio("4. هل تلتزم الجمعية بتوفير فني مقيم للمحطة؟", ["نعم", "لا"], index=1)
    
    # منطق الاستبعاد الصارم
    if "لا" in [q1, q2, q3, q4]:
        st.error("❌ عذراً، هذه المحطة غير مؤهلة للمشروع بسبب عدم استيفاء شروط التعاون.")
        st.stop() # يمنع الفني من إكمال باقي البيانات
    else:
        st.success("✅ الجمعية مستوفية لشروط الالتزام. يمكنك الانتقال لتبويب الفحص الفني.")

# --- التبويب الثاني: الفحص الفني (Technical Audit) ---
with tab2:
    st.header("⚙️ المواصفات الفنية الحالية للمحطة")
    
    # المعالجة الأولية
    with st.expander("1. منظومة المعالجة الأولية (Pre-treatment)"):
        c1, c2 = st.columns(2)
        with c1:
            hp_motor = st.number_input("قدرة الموتور الابتدائي (حصان)", value=1.5, step=0.5)
            vessel_count = st.number_input("عدد الخزانات (Vessels)", value=3, step=1)
            head_type = st.selectbox("نوع الهدود", ["يدوي (Manual)", "أوتوماتيك (Automatic)"])
        with c2:
            motor_flow = st.number_input("تدفق الموتور الابتدائي (م3/ساعة)", value=2.0)
            vessel_size = st.text_input("مقاس الخزانات (Vessel Size)", "1054")
            dosing_pumps = st.number_input("عدد مضخات الحقن (كلور/مانع ترسيب)", value=2, step=1)

    # وحدة الـ RO
    with st.expander("2. وحدة التناضح العكسي (RO Unit)"):
        c3, c4 = st.columns(2)
        with c3:
            h_pump_type = st.text_input("نوع طلمبة الضغط العالي")
            mem_count = st.number_input("إجمالي عدد الممبرينات", value=1, step=1)
            vessel_config = st.number_input("المحتوى الرأسي (عدد الممبرينات داخل الفيزل)", value=1)
        with c4:
            mem_type = st.text_input("موديل الممبرين", "BW30-4040")
            cartridge_size = st.selectbox("مقاس الشمع القطني", ["10 بوصة", "20 بوصة", "40 بوصة"])
            cart_count = st.number_input("عدد الشمعات داخل الهاوسينج", value=1)

    # القراءات والضغوط
    with st.expander("3. الضغوط والتحاليل اللحظية"):
        c5, c6 = st.columns(2)
        with c5:
            feed_tds = st.number_input("ملوحة الدخول (Feed TDS) - ppm", value=1000)
            perm_tds = st.number_input("ملوحة المنتج (Permeate TDS) - ppm", value=50)
            elec_status = st.selectbox("حالة الكهرباء", ["ثابتة", "غير مستقرة (تحتاج استبليزر)"])
        with c6:
            p_feed = st.number_input("ضغط الدخول (Feed Pressure) - Bar", value=0.0)
            p_brine = st.number_input("ضغط الأملاح (Brine Pressure) - Bar", value=0.0)
            p_perm = st.number_input("ضغط المنتج (Permeate Pressure) - Bar", value=0.0)

# --- التبويب الثالث: اللوجستيات (Logistics & Demographics) ---
with tab3:
    st.header("🗺️ الدراسة الاستراتيجية للموقع")
    
    col_pop1, col_pop2 = st.columns(2)
    with col_pop1:
        pop_count = st.number_input("تعداد سكان القرية المستهدفة", value=15000, step=1000)
        current_st = st.number_input("عدد المحطات العاملة حالياً بالقرية", value=1, step=1)
    
    with col_pop2:
        # حساب فجوة الاحتياج بناءً على معيار (15 ألف نسمة لكل محطة)
        ideal_count = pop_count / 15000
        gap = ideal_count - current_st
        st.metric("فجوة الاحتياج", f"{gap:.1f} محطة إضافية مطلوب تطويرها")

    st.markdown("---")
    loc_pos = st.radio("موقع المحطة بالنسبة للسكان", ["وسط الكتلة السكنية", "متطرف (بعيد عن الناس)"])
    access_way = st.select_slider("مدى سهولة وصول التروسيكل والجراكن", options=["مستحيل", "صعب", "متاح", "سهل جداً"])

# --- التبويب الرابع: التقرير ورأي المستكشف ---
with tab4:
    st.header("✍️ التقييم النهائي ورؤية المستكشف")
    
    insp_score = st.slider("تقييم 'جدية واهتمام' إدارة الجمعية (من 10)", 0, 10, 5)
    insp_notes = st.text_area("ملاحظاتك الفنية وانطباعك الشخصي", placeholder="اكتب هنا أي تفاصيل لم تشملها الأرقام (أصوات، نظافة، حالة المبنى...)")
    
    if st.button("اعتماد وحفظ تقييم المحطة 📥"):
        st.balloons()
        st.success("تم تسجيل بيانات الفحص بنجاح. جاري إرسال التقرير للمكتب الفني.")
        st.info(f"المحطة: {pop_count} نسمة | فجوة الاحتياج: {gap:.1f} | تقييم الإدارة: {insp_score}/10")