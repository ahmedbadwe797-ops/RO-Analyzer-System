import streamlit as st

# إعداد واجهة الموقع
st.set_page_config(page_title="Wamen Alma Hayah Portal", page_icon="💧")

st.title("💧 RO Station Performance Dashboard")
st.markdown("---")

# مدخلات البيانات من المهندس
st.sidebar.header("Station Data Input")
station = st.sidebar.text_input("Station Name", "Main Plant")
f_tds = st.sidebar.number_input("Feed TDS (ppm)", value=1000.0)
p_tds = st.sidebar.number_input("Permeate TDS (ppm)", value=50.0)
f_flow = st.sidebar.number_input("Feed Flow (m3/hr)", value=100.0)
p_flow = st.sidebar.number_input("Permeate Flow (m3/hr)", value=75.0)

# الحسابات الهندسية
if f_tds > 0 and f_flow > 0:
    rejection = ((f_tds - p_tds) / f_tds) * 100
    recovery = (p_flow / f_flow) * 100

    # عرض النتائج بشكل احترافي
    st.subheader(f"📊 Report for: {station}")
    c1, c2 = st.columns(2)
    c1.metric("Salt Rejection", f"{rejection:.2f}%")
    c2.metric("Recovery Rate", f"{recovery:.2f}%")

    if rejection < 98.5:
        st.error("🚨 Low Rejection! Check membranes immediately.")
    else:
        st.success("✅ Performance is optimal.")