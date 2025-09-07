import pandas as pd

def kpis(df: pd.DataFrame):
    active = int((df["status"] == "active").sum())
    hours = int(df["training_hours"].sum())
    completion = int(100 * df["completed_courses"].sum() / max(df["assigned_courses"].sum(), 1))
    return dict(active=active, hours=hours, completion=completion, models_active=12)

def by_department(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("department", as_index=False)
              .agg(training_hours=("training_hours","sum"))
              .sort_values("training_hours", ascending=False))