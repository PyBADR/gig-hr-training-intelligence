import argparse, os, re, pathlib

BANNER = "[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]({url})"
DEMO   = "## 🚀 Live Demo\n**[{url}]({url})**"

def upsert_readme(readme_path: str, url: str) -> bool:
    p = pathlib.Path(readme_path)
    txt = p.read_text(encoding="utf-8") if p.exists() else "# GIG HR Training Intelligence\n"
    # 1) Badge under H1
    if "Streamlit App" in txt:
        txt = re.sub(r"\[!\[Streamlit App\]\([^)]+\)\]\([^)]+\)", BANNER.format(url=url), txt, count=1)
    else:
        txt = re.sub(r"^(# .+?\n)", r"\1\n" + BANNER.format(url=url) + "\n\n", txt, count=1, flags=re.M)
    # 2) Live Demo section
    if "## 🚀 Live Demo" in txt:
        txt = re.sub(r"## 🚀 Live Demo.*?(?=\n## |\Z)", DEMO.format(url=url), txt, flags=re.S)
    else:
        txt += "\n\n" + DEMO.format(url=url) + "\n"
    p.write_text(txt, encoding="utf-8")
    return True

def upsert_app_caption(app_path: str, url: str) -> bool:
    p = pathlib.Path(app_path)
    if not p.exists(): return False
    txt = p.read_text(encoding="utf-8")
    if "Live Dashboard:" in txt: return False
    snippet = (
        "import os\n"
        "LIVE_URL = os.getenv('STREAMLIT_APP_URL', '{url}')\n"
        "import streamlit as st\n"
        "st.caption(f\"🔗 **Live Dashboard:** [{LIVE_URL}]({LIVE_URL})\")\n"
    ).format(url=url)
    m = re.search(r"(^(\s*import .+\n|\s*from .+ import .+\n)+)", txt, flags=re.M)
    if m:
        pos = m.end()
        txt = txt[:pos] + "\n" + snippet + "\n" + txt[pos:]
    else:
        txt = snippet + "\n" + txt
    p.write_text(txt, encoding="utf-8")
    return True

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--readme", default="README.md")
    ap.add_argument("--app", default="app.py")
    args = ap.parse_args()
    changed = upsert_readme(args.readme, args.url) | upsert_app_caption(args.app, args.url)
    print("Updated:", changed)
