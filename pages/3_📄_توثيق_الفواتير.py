# 3_📄_توثيق_الفواتير.py content
import streamlit as st, os, uuid, logging
import pandas as pd
from datetime import date
from PIL import Image
import streamlit.components.v1 as components
from utils.helpers import read_excel, write_excel

st.set_page_config(layout="centered", page_title="توثيق الفواتير")
st.markdown("<h2 dir='rtl' style='text-align:right;'>📄 توثيق الفواتير</h2>", unsafe_allow_html=True)

INVOICE_FILE = "data/invoices.xlsx"
IMG_DIR = "data/invoices"
os.makedirs(IMG_DIR, exist_ok=True)

tasks_df = read_excel("data/tasks.xlsx")
total_tasks = tasks_df["التكلفة"].sum() if not tasks_df.empty else 0
st.markdown(f"### 💰 تكلفة المهام الإجمالية: {total_tasks:,.2f}")

df_inv = read_excel(INVOICE_FILE, cols=["التاريخ","اسم الفاتورة","القيمة","الصورة"])

with st.form("inv_form", clear_on_submit=True):
    dat = st.date_input("تاريخ الفاتورة", value=date.today())
    name = st.text_input("اسم الفاتورة")
    val = st.number_input("القيمة", min_value=0.0)
    img = st.file_uploader("صورة الفاتورة", type=["jpg","png"], key="up2")
    sub = st.form_submit_button("إضافة")
    if sub:
        if not img or not name.strip() or val<=0:
            st.error("اكمل جميع الحقول")
        else:
            im = Image.open(img).convert("RGB")
            if im.width > 600:
                ratio = 600/im.width
                im = im.resize((600, int(im.height*ratio)))
            fname = f"{uuid.uuid4()}.jpg"
            im.save(os.path.join(IMG_DIR, fname), quality=85)
            df_inv = pd.concat([df_inv, pd.DataFrame([{"التاريخ": dat, "اسم الفاتورة": name, "القيمة": val, "الصورة": fname}])], ignore_index=True)
            write_excel(df_inv, INVOICE_FILE)
            st.success("✅ تمت إضافة الفاتورة")
            st.experimental_rerun()

st.subheader("📋 الفواتير")
total_inv = df_inv["القيمة"].sum() if not df_inv.empty else 0

if df_inv.empty:
    st.info("لا توجد فواتير")
else:
    for i, r in df_inv.iterrows():
        cols = st.columns([1,4,1])
        path = os.path.join(IMG_DIR, r["الصورة"])
        with cols[0]:
            if os.path.exists(path): st.image(path, width=200)
        with cols[1]:
            st.markdown(f"<div dir='rtl' style='text-align:right;'>📅 {r['التاريخ']}<br>📄 {r['اسم الفاتورة']}<br>💵 {r['القيمة']:,.2f}</div>", unsafe_allow_html=True)
        with cols[2]:
            if st.button("🗑️ حذف", key=f"delinv_{i}"):
                os.remove(path)
                df_inv = df_inv.drop(i).reset_index(drop=True)
                write_excel(df_inv, INVOICE_FILE)
                st.experimental_rerun()

st.markdown(f"### 💳 مجموع الفواتير: {total_inv:,.2f}")
st.markdown(f"### 🧾 المتبقي: {total_tasks - total_inv:,.2f}")
