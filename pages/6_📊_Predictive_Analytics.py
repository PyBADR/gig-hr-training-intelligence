"""
Predictive Analytics Dashboard
Attrition and Performance Prediction Models for Gulf Takaful
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import joblib
from pathlib import Path
try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
except ModuleNotFoundError:
    st.error("scikit-learn is not installed. Run: `pip install -r requirements.txt`")
    st.stop()
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Predictive Analytics - Gulf Takaful", page_icon="📊", layout="wide")

def generate_employee_data():
    """Generate sample employee data for prediction models"""
    np.random.seed(42)
    n_employees = 500
    
    departments = ['IT', 'HR', 'Finance', 'Operations', 'Claims', 'Underwriting', 'Sales', 'Legal', 'Investment', 'Customer Service']
    job_levels = ['Junior', 'Mid', 'Senior', 'Manager', 'Director']
    
    data = {
        'employee_id': [f'EMP_{i:03d}' for i in range(1, n_employees + 1)],
        'department': np.random.choice(departments, n_employees),
        'job_level': np.random.choice(job_levels, n_employees),
        'years_experience': np.random.randint(1, 20, n_employees),
        'age': np.random.randint(22, 60, n_employees),
        'training_hours_completed': np.random.randint(0, 120, n_employees),
        'performance_score': np.random.uniform(60, 100, n_employees),
        'satisfaction_score': np.random.uniform(3.0, 5.0, n_employees),
        'salary_band': np.random.randint(1, 10, n_employees),
        'promotion_last_2_years': np.random.choice([0, 1], n_employees, p=[0.7, 0.3]),
        'overtime_hours': np.random.randint(0, 50, n_employees),
        'sick_days': np.random.randint(0, 15, n_employees),
        'manager_rating': np.random.uniform(3.0, 5.0, n_employees)
    }
    
    # Create attrition target (influenced by various factors)
    attrition_prob = (
        (data['satisfaction_score'] < 3.5) * 0.3 +
        (data['performance_score'] < 70) * 0.2 +
        (data['years_experience'] > 15) * 0.1 +
        (data['overtime_hours'] > 30) * 0.2 +
        (data['promotion_last_2_years'] == 0) * 0.15
    )
    data['attrition'] = np.random.binomial(1, np.clip(attrition_prob, 0, 0.4), n_employees)
    
    return pd.DataFrame(data)

def train_attrition_model(data):
    """Train attrition prediction model"""
    # Prepare features
    le_dept = LabelEncoder()
    le_level = LabelEncoder()
    
    features = data.copy()
    features['department_encoded'] = le_dept.fit_transform(features['department'])
    features['job_level_encoded'] = le_level.fit_transform(features['job_level'])
    
    X = features[['department_encoded', 'job_level_encoded', 'years_experience', 'age',
                  'training_hours_completed', 'performance_score', 'satisfaction_score',
                  'salary_band', 'promotion_last_2_years', 'overtime_hours', 'sick_days', 'manager_rating']]
    y = features['attrition']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    
    return model, le_dept, le_level, accuracy

def train_performance_model(data):
    """Train performance prediction model"""
    le_dept = LabelEncoder()
    le_level = LabelEncoder()
    
    features = data.copy()
    features['department_encoded'] = le_dept.fit_transform(features['department'])
    features['job_level_encoded'] = le_level.fit_transform(features['job_level'])
    
    X = features[['department_encoded', 'job_level_encoded', 'years_experience', 'age',
                  'training_hours_completed', 'satisfaction_score', 'salary_band',
                  'promotion_last_2_years', 'overtime_hours', 'sick_days', 'manager_rating']]
    y = features['performance_score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    
    return model, le_dept, le_level, score

# Initialize session state
if 'employee_data' not in st.session_state:
    st.session_state.employee_data = generate_employee_data()
    
if 'attrition_model' not in st.session_state:
    with st.spinner("Training attrition prediction model..."):
        model, le_dept, le_level, accuracy = train_attrition_model(st.session_state.employee_data)
        st.session_state.attrition_model = model
        st.session_state.attrition_le_dept = le_dept
        st.session_state.attrition_le_level = le_level
        st.session_state.attrition_accuracy = accuracy

if 'performance_model' not in st.session_state:
    with st.spinner("Training performance prediction model..."):
        model, le_dept, le_level, score = train_performance_model(st.session_state.employee_data)
        st.session_state.performance_model = model
        st.session_state.performance_le_dept = le_dept
        st.session_state.performance_le_level = le_level
        st.session_state.performance_score = score

# Main Dashboard
st.title("📊 Predictive Analytics Dashboard")
st.markdown("AI-powered predictions for employee attrition and performance forecasting")

# Model Performance Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Attrition Model Accuracy", f"{st.session_state.attrition_accuracy:.1%}")
with col2:
    st.metric("Performance Model R²", f"{st.session_state.performance_score:.3f}")
with col3:
    high_risk_count = len(st.session_state.employee_data[st.session_state.employee_data['attrition'] == 1])
    st.metric("High Risk Employees", high_risk_count)
with col4:
    avg_performance = st.session_state.employee_data['performance_score'].mean()
    st.metric("Avg Performance Score", f"{avg_performance:.1f}")

st.divider()

# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["🚨 Attrition Risk", "📈 Performance Prediction", "📊 Analytics Overview", "🎯 Individual Prediction"])

with tab1:
    st.subheader("Employee Attrition Risk Analysis")
    
    # Attrition risk by department
    dept_attrition = st.session_state.employee_data.groupby('department')['attrition'].agg(['mean', 'count']).reset_index()
    dept_attrition['risk_percentage'] = dept_attrition['mean'] * 100
    
    fig_dept_risk = px.bar(
        dept_attrition,
        x='department',
        y='risk_percentage',
        title="Attrition Risk by Department",
        labels={'risk_percentage': 'Attrition Risk (%)', 'department': 'Department'}
    )
    fig_dept_risk.update_xaxes(tickangle=45)
    st.plotly_chart(fig_dept_risk, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk factors analysis
        high_risk = st.session_state.employee_data[st.session_state.employee_data['attrition'] == 1]
        low_risk = st.session_state.employee_data[st.session_state.employee_data['attrition'] == 0]
        
        risk_factors = pd.DataFrame({
            'Factor': ['Satisfaction Score', 'Performance Score', 'Training Hours', 'Overtime Hours'],
            'High Risk Avg': [
                high_risk['satisfaction_score'].mean(),
                high_risk['performance_score'].mean(),
                high_risk['training_hours_completed'].mean(),
                high_risk['overtime_hours'].mean()
            ],
            'Low Risk Avg': [
                low_risk['satisfaction_score'].mean(),
                low_risk['performance_score'].mean(),
                low_risk['training_hours_completed'].mean(),
                low_risk['overtime_hours'].mean()
            ]
        })
        
        fig_factors = go.Figure()
        fig_factors.add_trace(go.Bar(name='High Risk', x=risk_factors['Factor'], y=risk_factors['High Risk Avg']))
        fig_factors.add_trace(go.Bar(name='Low Risk', x=risk_factors['Factor'], y=risk_factors['Low Risk Avg']))
        fig_factors.update_layout(title='Risk Factors Comparison', barmode='group')
        st.plotly_chart(fig_factors, use_container_width=True)
    
    with col2:
        # High-risk employees table
        st.markdown("**High-Risk Employees (Top 10)**")
        
        # Predict attrition for all employees
        data_encoded = st.session_state.employee_data.copy()
        data_encoded['department_encoded'] = st.session_state.attrition_le_dept.transform(data_encoded['department'])
        data_encoded['job_level_encoded'] = st.session_state.attrition_le_level.transform(data_encoded['job_level'])
        
        X_pred = data_encoded[['department_encoded', 'job_level_encoded', 'years_experience', 'age',
                              'training_hours_completed', 'performance_score', 'satisfaction_score',
                              'salary_band', 'promotion_last_2_years', 'overtime_hours', 'sick_days', 'manager_rating']]
        
        attrition_probs = st.session_state.attrition_model.predict_proba(X_pred)[:, 1]
        
        high_risk_df = st.session_state.employee_data.copy()
        high_risk_df['attrition_risk'] = attrition_probs
        high_risk_df = high_risk_df.nlargest(10, 'attrition_risk')[['employee_id', 'department', 'job_level', 'attrition_risk']]
        high_risk_df['attrition_risk'] = high_risk_df['attrition_risk'].apply(lambda x: f"{x:.1%}")
        
        st.dataframe(high_risk_df, use_container_width=True)

with tab2:
    st.subheader("Performance Prediction Analysis")
    
    # Performance by department
    dept_performance = st.session_state.employee_data.groupby('department')['performance_score'].agg(['mean', 'std']).reset_index()
    
    fig_dept_perf = px.bar(
        dept_performance,
        x='department',
        y='mean',
        error_y='std',
        title="Average Performance Score by Department",
        labels={'mean': 'Average Performance Score', 'department': 'Department'}
    )
    fig_dept_perf.update_xaxes(tickangle=45)
    st.plotly_chart(fig_dept_perf, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance vs Training correlation
        fig_corr = px.scatter(
            st.session_state.employee_data,
            x='training_hours_completed',
            y='performance_score',
            color='department',
            title="Performance vs Training Hours",
            trendline="ols"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        # Top performers
        st.markdown("**Top Performers (Top 10)**")
        top_performers = st.session_state.employee_data.nlargest(10, 'performance_score')[['employee_id', 'department', 'job_level', 'performance_score']]
        top_performers['performance_score'] = top_performers['performance_score'].round(1)
        st.dataframe(top_performers, use_container_width=True)

with tab3:
    st.subheader("Predictive Analytics Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Feature importance for attrition
        feature_names = ['Department', 'Job Level', 'Experience', 'Age', 'Training Hours', 
                        'Performance', 'Satisfaction', 'Salary Band', 'Promotion', 'Overtime', 'Sick Days', 'Manager Rating']
        importance_scores = st.session_state.attrition_model.feature_importances_
        
        fig_importance = px.bar(
            x=importance_scores,
            y=feature_names,
            orientation='h',
            title="Feature Importance for Attrition Prediction"
        )
        st.plotly_chart(fig_importance, use_container_width=True)
    
    with col2:
        # Risk distribution
        risk_bins = pd.cut(attrition_probs, bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0], labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        risk_dist = risk_bins.value_counts()
        
        fig_risk_dist = px.pie(
            values=risk_dist.values,
            names=risk_dist.index,
            title="Attrition Risk Distribution"
        )
        st.plotly_chart(fig_risk_dist, use_container_width=True)

with tab4:
    st.subheader("Individual Employee Prediction")
    
    # Employee selection
    selected_emp = st.selectbox("Select Employee", st.session_state.employee_data['employee_id'].tolist())
    
    if selected_emp:
        emp_data = st.session_state.employee_data[st.session_state.employee_data['employee_id'] == selected_emp].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Employee Profile: {selected_emp}**")
            st.write(f"Department: {emp_data['department']}")
            st.write(f"Job Level: {emp_data['job_level']}")
            st.write(f"Experience: {emp_data['years_experience']} years")
            st.write(f"Current Performance: {emp_data['performance_score']:.1f}")
            st.write(f"Satisfaction: {emp_data['satisfaction_score']:.1f}/5.0")
        
        with col2:
            # Predict for this employee
            emp_encoded = emp_data.copy()
            emp_encoded['department_encoded'] = st.session_state.attrition_le_dept.transform([emp_data['department']])[0]
            emp_encoded['job_level_encoded'] = st.session_state.attrition_le_level.transform([emp_data['job_level']])[0]
            
            X_emp = [[emp_encoded['department_encoded'], emp_encoded['job_level_encoded'], emp_encoded['years_experience'],
                     emp_encoded['age'], emp_encoded['training_hours_completed'], emp_encoded['performance_score'],
                     emp_encoded['satisfaction_score'], emp_encoded['salary_band'], emp_encoded['promotion_last_2_years'],
                     emp_encoded['overtime_hours'], emp_encoded['sick_days'], emp_encoded['manager_rating']]]
            
            attrition_risk = st.session_state.attrition_model.predict_proba(X_emp)[0][1]
            
            # Performance prediction (excluding current performance)
            X_perf = [[emp_encoded['department_encoded'], emp_encoded['job_level_encoded'], emp_encoded['years_experience'],
                      emp_encoded['age'], emp_encoded['training_hours_completed'], emp_encoded['satisfaction_score'],
                      emp_encoded['salary_band'], emp_encoded['promotion_last_2_years'], emp_encoded['overtime_hours'],
                      emp_encoded['sick_days'], emp_encoded['manager_rating']]]
            
            predicted_performance = st.session_state.performance_model.predict(X_perf)[0]
            
            st.metric("Attrition Risk", f"{attrition_risk:.1%}")
            st.metric("Predicted Performance", f"{predicted_performance:.1f}")
            
            # Risk level
            if attrition_risk > 0.6:
                st.error("🚨 High Risk - Immediate attention required")
            elif attrition_risk > 0.4:
                st.warning("⚠️ Medium Risk - Monitor closely")
            else:
                st.success("✅ Low Risk - Employee likely to stay")

st.divider()
st.markdown("""
**📈 Model Insights:**
- Attrition model uses Random Forest with 12 key features
- Performance model uses Gradient Boosting for continuous prediction
- Models are retrained monthly with new data
- Predictions help HR make proactive decisions
""")