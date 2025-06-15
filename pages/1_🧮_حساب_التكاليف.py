# 1_🧮_حساب_التكاليف.py content
import streamlit as st
import pandas as pd
import os
from utils.helpers import read_excel, write_excel

st.set_page_config(layout="centered", page_title="حساب التكاليف")
st.markdown("<h2 dir='rtl' style='text-align:right;'>🧮 حساب التكاليف</h2>", unsafe_allow_html=True)

DATA_FILE = "data/tasks.xlsx"
os.makedirs("data", exist_ok=True)

@st.cache_data
def load_tasks():
    return read_excel(DATA_FILE, cols=["اسم المهمة", "العدد", "سعر الوحدة", "التكلفة"])

def save_tasks(df):
    write_excel(df, DATA_FILE)

if "df" not in st.session_state:
    st.session_state.df = load_tasks()

with st.form("task_form", clear_on_submit=True):
    name = st.text_input("اسم المهمة", key="name")
    count = st.number_input("العدد", min_value=1, value=1, key="count")
    price = st.number_input("سعر الوحدة", min_value=0.0, step=0.1, key="price")
    submit = st.form_submit_button("إضافة")
    if submit:
        if not name.strip():
            st.error("أدخل اسم المهمة")
        else:
            cost = price * count
            new = {"اسم المهمة": name, "العدد": count, "سعر الوحدة": price, "التكلفة": cost}
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new])], ignore_index=True)
            save_tasks(st.session_state.df)
            st.experimental_rerun()

st.subheader("📋 قائمة المهام")
if st.session_state.df.empty:
    st.info("لا توجد مهام حالياً")
else:
    total = st.session_state.df["التكلفة"].sum()
    st.dataframe(st.session_state.df)
    st.markdown(f"### 💰 التكلفة الإجمالية: {total:,.2f}")

area = st.number_input("المساحة بالمتر²", min_value=1.0, step=1.0)
if area > 0:
    st.markdown(f"### 💸 تكلفة الم²: {total/area:,.2f}")
