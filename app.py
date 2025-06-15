# app.py content
import streamlit as st

st.set_page_config(page_title="🏗️ توثيق مشروع بناء", layout="wide", page_icon="🏗️")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.form("pwd_form", clear_on_submit=False):
        pwd = st.text_input("🔒 كلمة المرور", type="password")
        sub = st.form_submit_button("دخول")
        if sub and pwd == "1234":
            st.session_state.authenticated = True
        elif sub:
            st.error("كلمة المرور غير صحيحة")
    st.stop()

st.markdown(
    """
    <div dir="rtl" style="text-align: right;">
      <h1>🏗️ تطبيق توثيق مشروع بناء عمارة</h1>
      <p><strong>إعداد: أنس الراجح</strong></p>
      <ul>
        <li>تسجيل المهام وتكاليفها</li>
        <li>توثيق المراحل بالصور</li>
        <li>إضافة فواتير ومتابعة التكلفة المتبقية</li>
      </ul>
      <p>🧾 استخدم القائمة الجانبية للتنقل بين الصفحات</p>
    </div>
    """, unsafe_allow_html=True)
