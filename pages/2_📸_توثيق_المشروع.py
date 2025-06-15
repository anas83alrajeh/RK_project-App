# 2_📸_توثيق_المشروع.py content
import streamlit as st
import os, uuid, logging
import pandas as pd
from datetime import date
from PIL import Image
import streamlit.components.v1 as components
from utils.helpers import read_excel, write_excel

st.set_page_config(layout="centered", page_title="توثيق المشروع")
st.markdown("<h2 dir='rtl' style='text-align:right;'>📸 توثيق المشروع</h2>", unsafe_allow_html=True)

DATA_DIR = "data/documentation"
META_FILE = os.path.join(DATA_DIR, "project_phases.xlsx")  # Or metadata.xlsx
os.makedirs(DATA_DIR, exist_ok=True)

def load_meta():
    return read_excel(META_FILE, cols=["الصورة", "الوصف", "التاريخ"])

def save_meta(df):
    write_excel(df, META_FILE)

df = load_meta()

with st.form("doc_form", clear_on_submit=True):
    img = st.file_uploader("رفع صورة", type=["jpg","png","jpeg"], key="up", label_visibility="collapsed")
    desc = st.text_input("الوصف")
    dat = st.date_input("التاريخ", value=date.today())
    sub = st.form_submit_button("إضافة")
    if sub:
        if not img or not desc.strip():
            st.error("يرفق صورة ووصف")
        else:
            im = Image.open(img).convert("RGB")
            fname = f"{uuid.uuid4()}.jpg"
            im.save(os.path.join(DATA_DIR, fname), quality=85)
            df = pd.concat([df, pd.DataFrame([{"الصورة": fname, "الوصف": desc, "التاريخ": dat}])], ignore_index=True)
            save_meta(df)
            st.experimental_rerun()

st.subheader("📑 الصور")
if df.empty:
    st.info("لا يوجد توثيق")
else:
    for i, r in df.iterrows():
        cols = st.columns([1,4,1])
        img_path = os.path.join(DATA_DIR, r["الصورة"])
        with cols[0]:
            if os.path.exists(img_path): st.image(img_path, caption=str(r["الوصف"]))
        with cols[1]:
            st.markdown(f"<div dir='rtl' style='text-align:right;'>📅 {r['التاريخ']}<br>📝 {r['الوصف']}</div>", unsafe_allow_html=True)
        with cols[2]:
            if st.button("🗑️ حذف", key=f"del_{i}"):
                os.remove(img_path)
                df = df.drop(i).reset_index(drop=True)
                save_meta(df)
                st.experimental_rerun()
