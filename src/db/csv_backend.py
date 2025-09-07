from pathlib import Path
import pandas as pd

def load_employees_csv() -> pd.DataFrame:
    p = Path(__file__).resolve().parents[2] / "data" / "employees_sample.csv"
    df = pd.read_csv(p)
    return df