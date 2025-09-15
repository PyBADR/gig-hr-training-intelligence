#!/usr/bin/env python3
from pathlib import Path
import pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

DATA = Path("data/training_records.csv")
OUTD = Path("models"); OUTD.mkdir(parents=True, exist_ok=True)
MODEL = OUTD / "completion_rf.joblib"

def main():
    if not DATA.exists():
        print("No data/training_records.csv — skip training."); return 0
    df = pd.read_csv(DATA)
    needed = {"Status","Department","Section","Provider","Hours","Cost_KWD","Quarter"}
    if not needed.issubset(df.columns):
        print(f"❌ training_records.csv missing columns: {needed - set(df.columns)}"); return 1
    df["Completed"] = (df["Status"].astype(str)=="Completed").astype(int)
    feats = ["Department","Section","Provider","Hours","Cost_KWD","Quarter"]
    X = df[feats].copy(); X["Quarter"]=X["Quarter"].astype(str); y=df["Completed"]

    cat,num=["Department","Section","Provider","Quarter"],["Hours","Cost_KWD"]
    pre=ColumnTransformer([("cat",OneHotEncoder(handle_unknown="ignore"),cat),("num","passthrough",num)])
    pipe=Pipeline([("prep",pre),("rf",RandomForestClassifier(n_estimators=200,random_state=42))])

    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
    pipe.fit(Xtr,ytr); f1=f1_score(yte,pipe.predict(Xte))
    joblib.dump(pipe,MODEL)
    print(f"✅ Saved {MODEL} | F1={f1:.3f}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
