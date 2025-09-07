import streamlit as st, folium
from streamlit_folium import st_folium
from src.services.employees import list_employees

st.set_page_config(page_title="Training Map")
df = st.cache_data(ttl=300)(list_employees)()
st.markdown("## Training Map")
m = folium.Map(location=[29.3759,47.9774], zoom_start=11, tiles="cartodbpositron")
for _, r in df[["lat","lon","name","city"]].dropna().iterrows():
    folium.CircleMarker([r["lat"],r["lon"]], radius=6, tooltip=r["name"]).add_to(m)
st_folium(m, width=1100, height=560)