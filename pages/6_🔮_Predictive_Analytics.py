import streamlit as st
from pathlib import Path

# Dependency guards
try:
    import joblib
except ModuleNotFoundError:
    try:
        from sklearn.externals import joblib  # legacy fallback
    except Exception:
        st.error("`joblib` is not installed. Run: `pip install -r requirements.txt`")
        st.stop()

try:
    from sklearn.ensemble import RandomForestClassifier  # noqa: F401
except ModuleNotFoundError:
    st.error("`scikit-learn` is not installed. Run: `pip install -r requirements.txt`")
    st.stop()

st.set_page_config(page_title="Predictive Analytics", layout="wide")
st.title("Predictive Analytics")

MODEL = Path("models/completion_rf.joblib")
DATA  = Path("data/training_records.csv")

# Train-or-load
pipe = None
if MODEL.exists():
    pipe = joblib.load(MODEL)
    st.success("Loaded trained completion model.")
elif DATA.exists():
    st.info("Model not found. Training from data/training_records.csv...")
    import subprocess, sys
    code = subprocess.call([sys.executable, "models/train_models.py"])
    if code==0 and MODEL.exists():
        pipe = joblib.load(MODEL)
        st.success("Model trained and loaded.")
    else:
        st.error("Training failed. Check data/training_records.csv columns.")
        st.stop()
else:
    st.warning("No model and no training data available. Please add data/training_records.csv.")
    st.stop()

# Inference UI
import pandas as pd, numpy as np
dept = st.text_input("Department", "Commercial Underwriting Department")
sect = st.text_input("Section", "General Insurance")
prov = st.text_input("Provider", "GIG Academy")
hours = st.number_input("Hours", 0, 100, 8)
cost  = st.number_input("Cost_KWD", 0, 10000, 120)
qtr   = st.selectbox("Quarter", ["Q1","Q2","Q3","Q4"])

if st.button("Predict Completion Likelihood"):
    X = pd.DataFrame([{
        "Department": dept, "Section": sect, "Provider": prov,
        "Hours": hours, "Cost_KWD": cost, "Quarter": qtr
    }])
    if hasattr(pipe, "predict_proba"):
        prob = pipe.predict_proba(X)[:,1]
    else:
        prob = np.clip(pipe.predict(X).astype(float), 0, 1)
    st.metric("Predicted Probability of Completion", f"{float(prob[0]):.0%}")
