import os
import streamlit as st
import plotly.express as px
from streamlit_folium import st_folium
import folium
from src.services.employees import list_employees
from src.services.analytics import kpis, by_department

st.set_page_config(page_title="GIG HR Training Intelligence", page_icon="📊", layout="wide")

# Sidebar
with st.sidebar:
    st.title("streamlit app")
    lang = st.selectbox("Language / اللغة", ["English", "العربية"])
    page = st.selectbox("Navigation", ["Dashboard"])
    st.caption(f"Backend: **{os.environ.get('DATA_BACKEND','csv').upper()}**")
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()

df = st.cache_data(ttl=300)(list_employees)()

# Dashboard
st.markdown("# GIG Takaful HR Training Intelligence")
st.caption("Smart Dashboard Powered by AI & Machine Learning")

k = kpis(df)
c1,c2,c3,c4 = st.columns(4)
c1.metric("Active Employees", k["active"])
c2.metric("Training Hours (Q4)", k["hours"])
c3.metric("Completion Rate", f"{k['completion']}%")
c4.metric("AI Predictions Active", k["models_active"])

st.markdown("### Kuwait Training Institutes Map")
m = folium.Map(location=[29.3759, 47.9774], zoom_start=11, tiles="cartodbpositron")
for _, r in df[["lat","lon","name","city"]].dropna().iterrows():
    folium.Marker([r["lat"], r["lon"]], tooltip=r["name"], popup=f"{r['name']} — {r['city']}").add_to(m)
st_folium(m, width=1000, height=420)

st.markdown("### Training Hours by Department")
dept = by_department(df)
fig = px.bar(dept, x="department", y="training_hours")
st.plotly_chart(fig, use_container_width=True)