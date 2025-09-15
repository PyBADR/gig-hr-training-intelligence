import pandas as pd
from pathlib import Path

def load_catalog():
    """Load training catalog from CSV file"""
    catalog_path = Path("data/training_catalog.csv")
    if catalog_path.exists():
        return pd.read_csv(catalog_path)
    else:
        # Return empty DataFrame with required columns if file doesn't exist
        return pd.DataFrame(columns=["Course","Provider","Department","Section","Level","Hours","Cost_KWD","Skills"])

# Business weights
W_COMPLETION = 0.50
W_COST_EFF  = 0.35
W_POPULAR   = 0.15

# Org-fit boosts
BOOST_DEPT, BOOST_SECT = 2.0, 1.5

CAT_REQ = ["Course","Provider","Department","Section","Level","Hours","Cost_KWD","Skills"]

def build_signals(catalog: pd.DataFrame, history: pd.DataFrame | None) -> pd.DataFrame:
    cat = catalog.copy()
    if history is not None and not history.empty:
        taken = history.groupby("Training Name").size().rename("taken")
        done  = history[history["Status"].eq("Completed")].groupby("Training Name").size().rename("done")
        sig   = pd.concat([taken, done], axis=1).fillna(0)
        sig["CompletionRate"] = sig["done"] / sig["taken"].replace(0, pd.NA)
        sig["CompletionRate"] = sig["CompletionRate"].fillna(0)
        sig["Popularity"]     = sig["taken"] / max(1, sig["taken"].sum())
        cat = cat.merge(sig, how="left", left_on="Course", right_index=True)
    else:
        cat["CompletionRate"] = 0.0
        cat["Popularity"]     = 0.0

    cost = cat["Cost_KWD"].astype(float).clip(lower=0)
    cat["CostEfficiency"] = 1 - (cost / cost.max()) if cost.max() > 0 else 0.0
    return cat.fillna({"CompletionRate":0.0,"Popularity":0.0,"CostEfficiency":0.0})

def recommend(emp_row, history, catalog, topn=8):
    miss = [c for c in CAT_REQ if c not in catalog.columns]
    if miss: raise ValueError(f"training_catalog.csv missing: {miss}")
    cat = build_signals(catalog, history)
    taken = set(history["Training Name"].unique()) if history is not None and not history.empty else set()
    df = cat[~cat["Course"].isin(taken)].copy()

    dept, sect = str(emp_row.get("Department","")), str(emp_row.get("Section",""))
    df["match_boost"] = BOOST_DEPT*(df["Department"]==dept) + BOOST_SECT*(df["Section"]==sect)

    df["score"] = (W_COMPLETION*df["CompletionRate"] +
                   W_COST_EFF *df["CostEfficiency"] +
                   W_POPULAR  *df["Popularity"] +
                   df["match_boost"])

    cols = ["Course","Provider","Department","Section","Level","Hours","Cost_KWD","Skills",
            "CompletionRate","CostEfficiency","Popularity","score"]
    return df.sort_values("score", ascending=False)[cols].head(topn)
