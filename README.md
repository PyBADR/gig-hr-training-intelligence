# GIG HR Training Intelligence System - Complete Setup Guide

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gig-hr-training-intelligence.streamlit.app)


## 🎯 **Project Overview**
A comprehensive HR training management system for GIG with 22 departments, 100 employees, real-time analytics, and ML-powered insights.

---

## 📦 **Quick Start Instructions**

### **Step 1: Create Project Directory**
```bash
mkdir gig-hr-training
cd gig-hr-training
```

### **Step 2: Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **Step 3: Install Requirements**
```bash
pip install streamlit pandas numpy plotly scikit-learn faker openpyxl
```

### **Step 4: Create Project Files**
1. Save the **Data Generator** code as `data_generator.py`
2. Save the **Streamlit Dashboard** code as `app.py`
3. Save the **Vercept Configuration** as `vercept.yaml`

### **Step 5: Generate Initial Data**
```bash
python data_generator.py
```
This creates:
- `training_records.csv` - Training data for 100 employees
- `departments.json` - All 22 departments
- `department_stats.csv` - Department-level statistics
- `ml_features.csv` - Features for ML models

### **Step 6: Launch Dashboard**
```bash
streamlit run app.py
```
Access at: http://localhost:8501

---

## 🏗️ **Complete Project Structure**

```
gig-hr-training/
│
├── app.py                    # Main Streamlit dashboard
├── data_generator.py         # Generate synthetic data
├── vercept.yaml             # Vercept deployment config
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
│
├── data/                   # Data directory
│   ├── training_records.csv
│   ├── departments.json
│   ├── department_stats.csv
│   └── ml_features.csv
│
├── models/                 # ML models directory
│   └── clustering_model.pkl
│
└── assets/                 # Static assets
    └── logo.png

```

---

## 🎨 **Dashboard Features**

### **1. Overview Tab**
- **KPI Cards**: Total Employees, Completed Trainings, Average Score, Completion Rate
- **Training Records Table**: Searchable, sortable, downloadable
- **Export Functionality**: Download as CSV

### **2. Analytics Tab**
- **Score by Department**: Bar chart showing average scores
- **Training Status**: Pie chart of completion status
- **Monthly Trends**: Line chart of training completions
- **Top Courses**: Most popular training programs

### **3. Employee Performance Tab**
- **Top Performers**: List of highest-scoring employees
- **Needs Improvement**: Employees requiring attention
- **Performance Metrics**: Individual completion rates

### **4. Add Record Tab**
- **Form Fields**:
  - Employee ID (EMP0001 format)
  - Employee Name
  - Department (dropdown)
  - Training Course (dropdown)
  - Completion Date
  - Score (0-100)
- **Auto Status**: Automatically sets Completed/In Progress based on score

### **5. ML Insights Tab**
- **Clustering Analysis**: 3D visualization of employee groups
- **Performance Categories**: High/Average/Needs Improvement
- **Cluster Statistics**: Detailed metrics for each group

---

## 🤖 **Machine Learning Components**

### **Clustering Algorithm**
```python
# KMeans clustering with 3 groups
features = ['avg_score', 'total_trainings', 'completed_trainings']
clusters = ['High Performer', 'Average Performer', 'Needs Improvement']
```

### **Feature Engineering**
- Average training score per employee
- Total number of trainings taken
- Completion rate percentage
- Department-level aggregations

---

## 🚀 **Vercept Deployment Instructions**

### **Method 1: Quick Deploy**
1. Upload all files to Vercept
2. Run: `vercept deploy --config vercept.yaml`
3. Access dashboard at provided URL

### **Method 2: Docker Deploy**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t gig-hr-training .
docker run -p 8501:8501 gig-hr-training
```

---

## 📊 **Department Structure**

### **Complete GIG Departments (22 Total)**

1. **Core Departments**
   - Engineering
   - Sales
   - Marketing
   - Human Resources
   - Finance

2. **Corporate Functions**
   - Legal Department
   - Information Technology
   - Corporate Communications
   - Investor Relations
   - Marketing & Public Relations

3. **HR Sub-units**
   - Talent, Training & Development

4. **Finance Related**
   - CFO Office
   - Director of Finance
   - Accounting

5. **Business Units**
   - Distribution
   - Individual Department
   - Commercial Underwriting
   - Life & Medical
   - Corporate Claims
   - Reinsurance

6. **Strategic Units**
   - Strategy & Digital Department
   - Risk Management

---

## 🔧 **Customization Options**

### **Add New Department**
Edit `DEPARTMENTS` list in `data_generator.py`:
```python
DEPARTMENTS.append("New Department Name")
```

### **Add New Training Course**
Edit `TRAINING_COURSES` list:
```python
TRAINING_COURSES.append("New Course Name")
```

### **Change Scoring Threshold**
In `app.py`, modify:
```python
status = "Completed" if score >= 60 else "In Progress"  # Change 60 to desired threshold
```

### **Adjust Cluster Count**
In clustering function:
```python
kmeans = KMeans(n_clusters=3)  # Change 3 to desired number
```

---

## 📈 **Performance Optimization**

### **Data Caching**
```python
@st.cache_data
def load_data():
    return pd.read_csv('training_records.csv')
```

### **Session State Management**
```python
if 'training_data' not in st.session_state:
    st.session_state.training_data = None
```

### **Batch Processing**
For large datasets (>10,000 records):
```python
chunk_size = 1000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)
```

---

## 🔍 **Troubleshooting**

### **Common Issues & Solutions**

1. **Dashboard not loading**
   - Check if all dependencies are installed
   - Verify data files exist in correct location
   - Ensure port 8501 is not in use

2. **Data not updating**
   - Clear Streamlit cache: Press 'C' in terminal
   - Restart the application
   - Check file permissions

3. **ML model errors**
   - Ensure scikit-learn is installed
   - Verify data has minimum 3 employees for clustering
   - Check for NaN values in features

---

## 📝 **Prompt Engineering for Vercept**

### **Essential Prompts**

1. **Deploy Dashboard**
```
Deploy GIG HR Training dashboard with 100 employees across 22 departments, 
including ML clustering and real-time analytics on Streamlit port 8501
```

2. **Generate Data**
```
Generate synthetic training data for 100 employees distributed across 
all GIG departments with scores between 50-100 and completion dates 
within the last 365 days
```

3. **Configure ML**
```
Setup KMeans clustering with 3 performance categories using average score, 
training count, and completion rate as features
```

4. **Schedule Updates**
```
Schedule daily data refresh at 6 AM and weekly ML model retraining 
every Sunday midnight
```

---

## ✅ **Success Checklist**

- [x] Project directory created
- [x] Virtual environment activated
- [x] Dependencies installed
- [x] Data generated (100 employees)
- [x] Dashboard running on localhost:8501
- [x] All 22 departments visible
- [x] Filters working (date, department, status)
- [x] Add new record functionality tested
- [x] ML clustering showing 3 groups
- [x] CSV export working
- [x] Charts displaying correctly
- [x] Search functionality operational

---

## 🎯 **Next Steps**

1. **Add Authentication**: Implement user login system
2. **Connect Database**: Replace CSV with MongoDB/PostgreSQL
3. **API Integration**: Add FastAPI backend
4. **Email Notifications**: Send training reminders
5. **Advanced ML**: Add predictive models for training success
6. **Multi-language**: Add Arabic support
7. **Mobile App**: Create responsive mobile version
8. **Real-time Updates**: Implement WebSocket connections

---

## 📞 **Support & Resources**

- **Documentation**: Review Streamlit docs at https://docs.streamlit.io
- **ML Resources**: Scikit-learn tutorials for clustering
- **Vercept Help**: Check vercept.yaml configuration
- **Data Issues**: Regenerate using data_generator.py

---

## 🏆 **Project Completion**

Your GIG HR Training Intelligence System is now ready! The dashboard provides:
- ✅ Complete department coverage (22 departments)
- ✅ 100 employee training records
- ✅ Real-time analytics and KPIs
- ✅ Machine learning insights
- ✅ Add/Edit functionality
- ✅ Export capabilities
- ✅ Interactive visualizations

**Launch Command**: `streamlit run app.py`
**Access URL**: http://localhost:8501

## 🚀 Live Demo
**[https://gig-hr-training-intelligence.streamlit.app](https://gig-hr-training-intelligence.streamlit.app)**