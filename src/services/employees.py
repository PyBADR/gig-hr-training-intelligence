import os
import pandas as pd
from typing import Literal
from ..db.csv_backend import load_employees_csv

BACKEND = os.environ.get("DATA_BACKEND", "csv").lower()

def list_employees() -> pd.DataFrame:
    if BACKEND == "supabase":
        from ..db.supabase_backend import load_employees_supabase
        try:
            df = load_employees_supabase()
            if df.empty:
                return load_employees_csv()
            return df
        except Exception:
            return load_employees_csv()
    return load_employees_csv()