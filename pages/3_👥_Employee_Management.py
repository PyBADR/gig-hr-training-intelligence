# pages/3_👥_Employee_Management.py
import streamlit as st
import pandas as pd
from lib.data_loader import employees

st.set_page_config(page_title="Employee Management", layout="wide")
st.title("Employee Management")

emp = employees()

# normalize and display core fields
core_cols = ["Employee Code","Employee Name","Department","Section","Job Tittle","Email"]
if not emp.empty:
    missing = [c for c in core_cols if c not in emp.columns]
    if missing:
        st.error(f"employees.csv missing columns: {missing}")
        st.stop()

    q = st.text_input("Search name/department/section")
    view = emp.copy()
    if q:
        ql = q.lower()
        view = view[
            view.apply(lambda r: ql in str(r["Employee Name"]).lower()
                                 or ql in str(r["Department"]).lower()
                                 or ql in str(r["Section"]).lower(), axis=1)
        ]
    st.dataframe(view[core_cols], use_container_width=True, height=480)
    st.download_button(
        "⬇️ Export employees.csv",
        data=emp[core_cols].to_csv(index=False).encode("utf-8"),
        file_name="employees.csv",
        mime="text/csv"
    )
else:
    st.info("Upload data/employees.csv with the core columns to enable this page.")