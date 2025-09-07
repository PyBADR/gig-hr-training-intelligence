import streamlit as st, plotly.express as px
from src.services.employees import list_employees
from src.services.analytics import by_department

df = st.cache_data(ttl=300)(list_employees)()
st.markdown("## Analytics Dashboard")
st.dataframe(df, use_container_width=True)
fig = px.line(by_department(df), x="department", y="training_hours", markers=True)
st.plotly_chart(fig, use_container_width=True)