# pages/5_🤖_AI_Recommendations.py
import streamlit as st
import pandas as pd
from lib.data_loader import employees, trainings, training_catalog
from models.recommender import load_catalog, recommend

st.set_page_config(page_title="AI Recommendations", layout="wide")
st.title("AI Recommendations")

emp = employees()
tr  = trainings()
cat = training_catalog()

if emp.empty:
    st.error("employees.csv not found.")
    st.stop()
if cat.empty:
    st.error("training_catalog.csv not found. Add it under data/ with columns: "
             "Course,Provider,Department,Section,Level,Hours,Cost_KWD,Skills")
    st.stop()

# select employee
sel = st.selectbox("Select Employee", emp["Employee Name"])
row = emp.loc[emp["Employee Name"].eq(sel)].iloc[0]
hist = tr.loc[tr["Employee Code"].astype(str) == str(row["Employee Code"])] if not tr.empty else pd.DataFrame()

st.subheader("Recommended Courses")
rec = recommend(row, hist, load_catalog(cat), topn=6)
st.dataframe(rec, use_container_width=True)

st.caption("Ranking = Department/Section match + popularity + cost efficiency")
