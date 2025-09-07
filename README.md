# GIG Takaful HR Training Intelligence

A production-grade Streamlit application for HR training analytics and management, deployable on Streamlit Community Cloud.

## Features

- 📊 Interactive dashboard with KPIs and analytics
- 🗺️ Training institutes map visualization
- 👥 Employee management with search and export
- 🔄 Flexible backend (CSV or Supabase)
- 🎨 Professional dark theme
- ⚡ Fast cold-start performance

## Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## GitHub Setup

```bash
# Initialize repository
git init
git add .
git commit -m "feat: streamlit community cloud scaffold"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/gig-hr-training-intelligence.git
git push -u origin main
```

## Streamlit Community Cloud Deployment

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository: `YOUR_USERNAME/gig-hr-training-intelligence`
4. Set branch: `main`
5. Set main file: `app.py`
6. (Optional) Configure secrets for Supabase:
   - Go to App → Settings → Secrets
   - Copy content from `.streamlit/secrets_template.toml`
   - Set `DATA_BACKEND="supabase"` and add your Supabase credentials
7. Click "Deploy"

## Configuration

### CSV Backend (Default)
No configuration needed. Uses sample data from `data/employees_sample.csv`.

### Supabase Backend
Set these environment variables in Streamlit Cloud secrets:

```toml
DATA_BACKEND = "supabase"
SUPABASE_URL = "your-supabase-url"
SUPABASE_ANON_KEY = "your-anon-key"
SUPABASE_EMP_TABLE = "employees"
```

## License

MIT License - see LICENSE file for details.