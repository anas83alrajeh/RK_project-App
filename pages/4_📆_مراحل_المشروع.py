# 4_📆_مراحل_المشروع.py content
import streamlit as st
import pandas as pd
import os
from utils.helpers import read_excel, write_excel

st.set_page_config(layout="centered", page_title="مراحل المشروع")
st.markdown("<h2 dir='rtl' style='text-align:right;'>📆 مراحل المشروع</h2>", unsafe_allow_html=True)

FILE = "data/project_phases.xlsx"
os.makedirs("data", exist_ok=True)

def default_phases():
    phases = [{"رقم": i+1, "اسم": n, "الوصف": d, "البداية": "", "النهاية": "", "المدة": ""} 
              for i,(n,d) in enumerate([
                  ("تحديد الأرض", "استكشاف الأرض"),
                  ("استخراج التراخيص", "استخراج التصاريح"),
                  ("التصميم", "تصميم معماري وإنشائي"),
                  ("الحفر", "أعمال الحفر"),
                  ("الأساسات", "صب القواعد"),
                  ("الإنشاءات", "صب الأعمدة والجدران"),
                  ("التشطيبات", "البناء والدهان"),
                  ("السباكة والكهرباء", "تمديدات داخلية"),
                  ("تركيب المصعد", "إنهاء جاهزية المصعد"),
                  ("تسليم المشروع", "إعداد تقرير التسليم")])]
    return pd.DataFrame(phases)

df = read_excel(FILE) if os.path.exists(FILE) else default_phases()

def safe_date(v): return pd.to_datetime(v).date() if v not in (None,"") else None

for i, r in df.iterrows():
    st.markdown(f"<b>المرحلة {r['رقم']} – {r['اسم']}</b>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    df.at[i,"البداية"] = st.date_input(f"بداية", value=safe_date(r["البداية"]), key=f"b_{i}")
    df.at[i,"النهاية"] = st.date_input(f"نهاية", value=safe_date(r["النهاية"]), key=f"e_{i}")
    if df.at[i,"البداية"] and df.at[i,"النهاية"]:
        df.at[i,"المدة"] = (pd.to_datetime(df.at[i,"النهاية"]) - pd.to_datetime(df.at[i,"البداية"])).days
    st.write(f"🕒 المدة: {df.at[i,'المدة']} يوم")

if st.button("💾 حفظ"):
    write_excel(df, FILE)
    st.success("✅ تم الحفظ")

total = len(df[df["المدة"]!=""])
pct = total / len(df) * 100
st.markdown(f"### ✅ نسبة الإنجاز: {pct:.0f}%")
