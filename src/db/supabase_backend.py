import os
import pandas as pd
from supabase import create_client

def _client():
    url = os.environ.get("SUPABASE_URL") or ""
    key = os.environ.get("SUPABASE_ANON_KEY") or ""
    if not url or not key:
        raise RuntimeError("Supabase credentials missing")
    return create_client(url, key)

def load_employees_supabase() -> pd.DataFrame:
    table = os.environ.get("SUPABASE_EMP_TABLE", "employees")
    sb = _client()
    res = sb.table(table).select("*").execute()
    return pd.DataFrame(res.data or [])