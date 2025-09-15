#!/usr/bin/env python3
import pandas as pd, sys, argparse
from pathlib import Path

REQ = ["Course","Provider","Department","Section","Level","Hours","Cost_KWD","Skills"]

def load_any(p: Path) -> pd.DataFrame:
    if p.suffix.lower()==".csv": return pd.read_csv(p)
    xls = pd.ExcelFile(p); sheet = "TrainingCatalog" if "TrainingCatalog" in xls.sheet_names else xls.sheet_names[0]
    return pd.read_excel(p, sheet_name=sheet)

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    mapping = {"Course Name":"Course","Title":"Course","Provider Name":"Provider",
               "Dept":"Department","Dept.":"Department","Sec":"Section",
               "Duration":"Hours","Cost (KWD)":"Cost_KWD","Cost":"Cost_KWD"}
    df = df.rename(columns={k:v for k,v in mapping.items() if k in df.columns})
    miss = [c for c in REQ if c not in df.columns]
    if miss: sys.exit(f"❌ Missing columns: {miss} | Present: {list(df.columns)}")
    df["Hours"]    = pd.to_numeric(df["Hours"], errors="coerce").fillna(0)
    df["Cost_KWD"] = pd.to_numeric(df["Cost_KWD"], errors="coerce").fillna(0)
    df["Level"]    = df["Level"].astype(str).str.title()
    df["Skills"]   = df["Skills"].fillna("").astype(str).str.replace(",", ";")
    return df[REQ]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="catalog.xlsx or catalog.csv")
    ap.add_argument("--outdir", default="data")
    a = ap.parse_args()
    outdir = Path(a.outdir); outdir.mkdir(parents=True, exist_ok=True)
    df = normalize(load_any(Path(a.input)))
    out = outdir / "training_catalog.csv"
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"✅ Wrote {out} ({len(df)} rows)"); print(df.head(3))

if __name__ == "__main__":
    main()
