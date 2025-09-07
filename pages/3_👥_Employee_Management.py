import streamlit as st
from src.services.employees import list_employees

df = st.cache_data(ttl=300)(list_employees)()
st.markdown("## Employee Management")
q = st.text_input("Search name/department")
if q:
    m = df.apply(lambda r: q.lower() in " ".join(map(str, r.values)).lower(), axis=1)
    df = df[m]
st.dataframe(df, use_container_width=True)
st.download_button("Export CSV", df.to_csv(index=False), file_name="employees_export.csv")