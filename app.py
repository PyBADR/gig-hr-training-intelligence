# app.py - GIG HR Training Intelligence Dashboard

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="GIG HR Training Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {padding-top: 1rem;}
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    div[data-testid="metric-container"] {
        background-color: rgba(28, 131, 225, 0.1);
        border: 2px solid rgba(28, 131, 225, 0.2);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
if 'training_data' not in st.session_state:
    st.session_state.training_data = None
if 'new_records' not in st.session_state:
    st.session_state.new_records = []

@st.cache_data
def load_departments():
    """Load department list"""
    departments = [
        "Engineering", "Sales", "Marketing", "Human Resources", "Finance",
        "Legal Department", "Information Technology", "Corporate Communications",
        "Investor Relations", "Marketing & Public Relations",
        "Talent, Training & Development", "CFO Office", "Director of Finance",
        "Accounting", "Distribution", "Individual Department",
        "Commercial Underwriting", "Life & Medical", "Corporate Claims",
        "Reinsurance", "Strategy & Digital Department", "Risk Management"
    ]
    return departments

@st.cache_data
def load_training_courses():
    """Load available training courses"""
    courses = [
        "AML & Compliance Basics", "Insurance Fraud Detection",
        "Advanced Excel for Analysts", "Customer Experience Excellence",
        "Underwriting Fundamentals", "Claims Management Essentials",
        "Cybersecurity Awareness", "Data Analytics for Business",
        "Leadership & Communication", "Reinsurance Principles"
    ]
    return courses

def generate_sample_data():
    """Generate sample training data"""
    from faker import Faker
    import random
    
    fake = Faker()
    departments = load_departments()
    courses = load_training_courses()
    
    records = []
    for i in range(1, 101):
        for j in range(random.randint(1, 3)):
            completion_date = pd.Timestamp.now() - pd.Timedelta(days=random.randint(1, 365))
            score = random.randint(50, 100)
            
            records.append({
                'employee_id': f'EMP{i:04d}',
                'employee_name': fake.name(),
                'department': random.choice(departments),
                'training_course': random.choice(courses),
                'completion_date': completion_date.date(),
                'score': score,
                'status': 'Completed' if score >= 60 else 'In Progress'
            })
    
    return pd.DataFrame(records)

def perform_clustering(df):
    """Perform KMeans clustering on employee performance"""
    # Aggregate by employee
    employee_metrics = df.groupby(['employee_id', 'employee_name', 'department']).agg({
        'score': ['mean', 'count'],
        'status': lambda x: (x == 'Completed').sum()
    }).reset_index()
    
    employee_metrics.columns = ['employee_id', 'employee_name', 'department', 
                                'avg_score', 'total_trainings', 'completed_trainings']
    
    # Prepare features for clustering
    features = employee_metrics[['avg_score', 'total_trainings', 'completed_trainings']]
    
    # Standardize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    employee_metrics['cluster'] = kmeans.fit_predict(features_scaled)
    
    # Label clusters
    cluster_labels = {0: 'High Performer', 1: 'Average Performer', 2: 'Needs Improvement'}
    employee_metrics['performance_category'] = employee_metrics['cluster'].map(cluster_labels)
    
    return employee_metrics

def main():
    # Header
    st.title("🎯 GIG HR Training Intelligence Dashboard")
    st.markdown("**Real-time Training Analytics & Machine Learning Insights**")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Dashboard Controls")
        
        # Data source selection
        data_source = st.radio(
            "Data Source",
            ["Generate Sample Data", "Upload CSV", "Use Session Data"]
        )
        
        if data_source == "Generate Sample Data":
            if st.button("Generate Data"):
                st.session_state.training_data = generate_sample_data()
                st.success("✅ Sample data generated!")
        
        elif data_source == "Upload CSV":
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            if uploaded_file is not None:
                st.session_state.training_data = pd.read_csv(uploaded_file)
                st.success("✅ Data uploaded successfully!")
        
        # Load data
        if st.session_state.training_data is None:
            st.session_state.training_data = generate_sample_data()
        
        df = st.session_state.training_data.copy()
        
        # Convert dates
        df['completion_date'] = pd.to_datetime(df['completion_date'])
        
        st.divider()
        
        # Filters
        st.header("📋 Filters")
        
        # Department filter
        departments = ["All"] + sorted(df['department'].unique().tolist())
        selected_dept = st.selectbox("Department", departments)
        
        # Date range filter
        min_date = df['completion_date'].min().date()
        max_date = df['completion_date'].max().date()
        
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Status filter
        status_filter = st.multiselect(
            "Training Status",
            ["Completed", "In Progress"],
            default=["Completed", "In Progress"]
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_dept != "All":
        filtered_df = filtered_df[filtered_df['department'] == selected_dept]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['completion_date'].dt.date >= start_date) &
            (filtered_df['completion_date'].dt.date <= end_date)
        ]
    
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    
    # Main Dashboard
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "📈 Analytics", "👥 Employee Performance", 
        "➕ Add Record", "🤖 ML Insights"
    ])
    
    with tab1:
        # KPI Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_employees = filtered_df['employee_id'].nunique()
            st.metric("Total Employees", total_employees)
        
        with col2:
            completed = filtered_df[filtered_df['status'] == 'Completed'].shape[0]
            st.metric("Completed Trainings", completed)
        
        with col3:
            avg_score = filtered_df['score'].mean()
            st.metric("Average Score", f"{avg_score:.1f}")
        
        with col4:
            completion_rate = (completed / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        st.divider()
        
        # Training Records Table
        st.subheader("📋 Training Records")
        
        # Display options
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("🔍 Search (Employee Name/ID/Course)", "")
        with col2:
            show_rows = st.selectbox("Show rows", [10, 25, 50, 100, "All"])
        
        # Apply search
        display_df = filtered_df.copy()
        if search:
            display_df = display_df[
                display_df['employee_name'].str.contains(search, case=False, na=False) |
                display_df['employee_id'].str.contains(search, case=False, na=False) |
                display_df['training_course'].str.contains(search, case=False, na=False)
            ]
        
        # Format date
        display_df['completion_date'] = display_df['completion_date'].dt.strftime('%Y-%m-%d')
        
        # Display table
        if show_rows == "All":
            st.dataframe(display_df, use_container_width=True, height=400)
        else:
            st.dataframe(display_df.head(show_rows), use_container_width=True, height=400)
        
        # Download button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f'training_records_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        )
    
    with tab2:
        st.subheader("📊 Training Analytics Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Training Score by Department
            dept_scores = filtered_df.groupby('department')['score'].mean().sort_values(ascending=True)
            fig1 = px.bar(
                x=dept_scores.values,
                y=dept_scores.index,
                orientation='h',
                title="Average Training Score by Department",
                labels={'x': 'Average Score', 'y': 'Department'},
                color=dept_scores.values,
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Training Status Distribution
            status_counts = filtered_df['status'].value_counts()
            fig2 = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Training Status Distribution",
                color_discrete_map={'Completed': '#2ecc71', 'In Progress': '#f39c12'}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly Training Completion Trend
            monthly_completion = filtered_df.copy()
            monthly_completion['month'] = monthly_completion['completion_date'].dt.to_period('M')
            monthly_trend = monthly_completion.groupby(['month', 'status']).size().reset_index(name='count')
            monthly_trend['month'] = monthly_trend['month'].astype(str)
            
            fig3 = px.line(
                monthly_trend,
                x='month',
                y='count',
                color='status',
                title="Monthly Training Completion Trend",
                markers=True
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Top Training Courses
            course_counts = filtered_df['training_course'].value_counts().head(10)
            fig4 = px.bar(
                x=course_counts.values,
                y=course_counts.index,
                orientation='h',
                title="Top 10 Training Courses",
                labels={'x': 'Number of Enrollments', 'y': 'Course'}
            )
            st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
        st.subheader("👥 Employee Performance Analysis")
        
        # Get employee performance metrics
        employee_metrics = filtered_df.groupby(['employee_id', 'employee_name', 'department']).agg({
            'score': ['mean', 'count'],
            'status': lambda x: (x == 'Completed').sum()
        }).reset_index()
        
        employee_metrics.columns = ['Employee ID', 'Name', 'Department', 
                                    'Avg Score', 'Total Trainings', 'Completed']
        
        employee_metrics['Completion Rate %'] = (
            employee_metrics['Completed'] / employee_metrics['Total Trainings'] * 100
        ).round(1)
        
        # Sort by average score
        employee_metrics = employee_metrics.sort_values('Avg Score', ascending=False)
        employee_metrics['Avg Score'] = employee_metrics['Avg Score'].round(1)
        
        # Top performers
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("🏆 **Top 10 Performers**")
            st.dataframe(
                employee_metrics.head(10)[['Name', 'Department', 'Avg Score', 'Completion Rate %']],
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.warning("📉 **Needs Improvement (Bottom 10)**")
            st.dataframe(
                employee_metrics.tail(10)[['Name', 'Department', 'Avg Score', 'Completion Rate %']],
                use_container_width=True,
                hide_index=True
            )
    
    with tab4:
        st.subheader("➕ Add New Training Record")
        
        with st.form("add_record_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                employee_id = st.text_input("Employee ID", placeholder="EMP0001")
                employee_name = st.text_input("Employee Name", placeholder="John Doe")
                department = st.selectbox("Department", load_departments())
            
            with col2:
                training_course = st.selectbox("Training Course", load_training_courses())
                completion_date = st.date_input("Completion Date", value=date.today())
                score = st.number_input("Score", min_value=0, max_value=100, value=80)
            
            with col3:
                st.write("")
                st.write("")
                status = "Completed" if score >= 60 else "In Progress"
                st.info(f"Status: **{status}**")
            
            submitted = st.form_submit_button("➕ Add Training Record", use_container_width=True)
            
            if submitted:
                if employee_id and employee_name:
                    new_record = pd.DataFrame([{
                        'employee_id': employee_id,
                        'employee_name': employee_name,
                        'department': department,
                        'training_course': training_course,
                        'completion_date': completion_date,
                        'score': score,
                        'status': status
                    }])
                    
                    st.session_state.training_data = pd.concat([
                        st.session_state.training_data, 
                        new_record
                    ], ignore_index=True)
                    
                    st.success("✅ Training record added successfully!")
                    st.balloons()
                else:
                    st.error("Please fill in all required fields!")
    
    with tab5:
        st.subheader("🤖 Machine Learning Insights")
        
        # Perform clustering
        cluster_df = perform_clustering(filtered_df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cluster distribution
            cluster_counts = cluster_df['performance_category'].value_counts()
            fig5 = px.pie(
                values=cluster_counts.values,
                names=cluster_counts.index,
                title="Employee Performance Clusters",
                color_discrete_map={
                    'High Performer': '#2ecc71',
                    'Average Performer': '#3498db',
                    'Needs Improvement': '#e74c3c'
                }
            )
            st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            # 3D Scatter plot of clusters
            fig6 = px.scatter_3d(
                cluster_df,
                x='avg_score',
                y='total_trainings',
                z='completed_trainings',
                color='performance_category',
                title="Employee Clustering Analysis",
                labels={
                    'avg_score': 'Average Score',
                    'total_trainings': 'Total Trainings',
                    'completed_trainings': 'Completed Trainings'
                },
                hover_data=['employee_name', 'department']
            )
            st.plotly_chart(fig6, use_container_width=True)
        
        # Cluster details
        st.subheader("📊 Cluster Analysis")
        
        for category in cluster_df['performance_category'].unique():
            category_df = cluster_df[cluster_df['performance_category'] == category]
            
            with st.expander(f"{category} ({len(category_df)} employees)"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Average Score", f"{category_df['avg_score'].mean():.1f}")
                with col2:
                    st.metric("Avg Trainings", f"{category_df['total_trainings'].mean():.1f}")
                with col3:
                    st.metric("Avg Completed", f"{category_df['completed_trainings'].mean():.1f}")
                
                st.dataframe(
                    category_df[['employee_name', 'department', 'avg_score', 'total_trainings']].head(10),
                    use_container_width=True,
                    hide_index=True
                )

if __name__ == "__main__":
    main()