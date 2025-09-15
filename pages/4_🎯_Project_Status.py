"""
Project Status Tracking Dashboard
Comprehensive project management and tracking for Gulf Takaful training initiatives
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="Project Status - Gulf Takaful", page_icon="🎯", layout="wide")

def create_project_summary_cards(projects_data):
    """Create summary KPI cards for projects"""
    
    total_projects = len(projects_data)
    active_projects = len([p for p in projects_data if p['status'] in ['PLANNED', 'IN_PROGRESS']])
    completed_projects = len([p for p in projects_data if p['status'] == 'COMPLETED'])
    total_budget = sum(p['total_budget'] for p in projects_data)
    total_spent = sum(p['spent_amount'] for p in projects_data)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Projects",
            value=total_projects,
            delta=f"+{np.random.randint(2, 8)} this quarter"
        )
    
    with col2:
        st.metric(
            label="Active Projects",
            value=active_projects,
            delta=f"{active_projects/total_projects*100:.1f}% of total" if total_projects > 0 else "0%"
        )
    
    with col3:
        completion_rate = (completed_projects / total_projects * 100) if total_projects > 0 else 0
        st.metric(
            label="Completion Rate",
            value=f"{completion_rate:.1f}%",
            delta=f"+{np.random.uniform(2, 8):.1f}% vs last quarter"
        )
    
    with col4:
        st.metric(
            label="Total Budget",
            value=f"KWD {total_budget:,.0f}",
            delta=f"KWD {np.random.randint(10000, 50000):,} allocated"
        )
    
    with col5:
        budget_utilization = (total_spent / total_budget * 100) if total_budget > 0 else 0
        st.metric(
            label="Budget Utilization",
            value=f"{budget_utilization:.1f}%",
            delta=f"{budget_utilization - 75:.1f}% vs target"
        )

def get_departments():
    """Get list of departments"""
    return [
        'Information Technology', 'Human Resources', 'Finance',
        'Operations', 'Claims', 'Underwriting', 'Sales & Marketing',
        'Legal & Compliance', 'Investment', 'Customer Service'
    ]

def get_projects_data(status_filter, dept_filter, priority_filter, year_filter):
    """Get filtered project data"""
    
    # Sample project data
    projects = [
        {
            'project_code': 'TRN-2024-001',
            'project_name': 'Digital Transformation Training Program',
            'department': 'Information Technology',
            'status': 'IN_PROGRESS',
            'priority': 'HIGH',
            'completion_percentage': 75,
            'total_budget': 150000,
            'spent_amount': 112500,
            'start_date': '2024-01-15',
            'planned_end_date': '2024-12-31',
            'roi_percentage': 25.5
        },
        {
            'project_code': 'TRN-2024-002',
            'project_name': 'Leadership Development Initiative',
            'department': 'Human Resources',
            'status': 'IN_PROGRESS',
            'priority': 'MEDIUM',
            'completion_percentage': 60,
            'total_budget': 85000,
            'spent_amount': 51000,
            'start_date': '2024-02-01',
            'planned_end_date': '2024-11-30',
            'roi_percentage': 18.2
        },
        {
            'project_code': 'TRN-2024-003',
            'project_name': 'Compliance Training Update',
            'department': 'Legal & Compliance',
            'status': 'COMPLETED',
            'priority': 'CRITICAL',
            'completion_percentage': 100,
            'total_budget': 45000,
            'spent_amount': 42000,
            'start_date': '2024-01-01',
            'planned_end_date': '2024-06-30',
            'roi_percentage': 35.8
        },
        {
            'project_code': 'TRN-2024-004',
            'project_name': 'Customer Service Excellence Program',
            'department': 'Customer Service',
            'status': 'IN_PROGRESS',
            'priority': 'HIGH',
            'completion_percentage': 45,
            'total_budget': 65000,
            'spent_amount': 29250,
            'start_date': '2024-03-01',
            'planned_end_date': '2024-10-31',
            'roi_percentage': 22.1
        },
        {
            'project_code': 'TRN-2024-005',
            'project_name': 'Financial Analysis & Reporting Skills',
            'department': 'Finance',
            'status': 'PLANNED',
            'priority': 'MEDIUM',
            'completion_percentage': 15,
            'total_budget': 75000,
            'spent_amount': 11250,
            'start_date': '2024-04-01',
            'planned_end_date': '2024-12-15',
            'roi_percentage': 0
        },
        {
            'project_code': 'TRN-2024-006',
            'project_name': 'Claims Processing Optimization',
            'department': 'Claims',
            'status': 'IN_PROGRESS',
            'priority': 'HIGH',
            'completion_percentage': 80,
            'total_budget': 95000,
            'spent_amount': 76000,
            'start_date': '2024-01-20',
            'planned_end_date': '2024-09-30',
            'roi_percentage': 28.7
        },
        {
            'project_code': 'TRN-2024-007',
            'project_name': 'Underwriting Excellence Program',
            'department': 'Underwriting',
            'status': 'IN_PROGRESS',
            'priority': 'MEDIUM',
            'completion_percentage': 55,
            'total_budget': 70000,
            'spent_amount': 38500,
            'start_date': '2024-02-15',
            'planned_end_date': '2024-11-15',
            'roi_percentage': 19.3
        },
        {
            'project_code': 'TRN-2024-008',
            'project_name': 'Sales & Marketing Mastery',
            'department': 'Sales & Marketing',
            'status': 'PLANNED',
            'priority': 'LOW',
            'completion_percentage': 10,
            'total_budget': 55000,
            'spent_amount': 5500,
            'start_date': '2024-05-01',
            'planned_end_date': '2024-12-31',
            'roi_percentage': 0
        },
        {
            'project_code': 'TRN-2024-009',
            'project_name': 'Investment Strategy Training',
            'department': 'Investment',
            'status': 'ON_HOLD',
            'priority': 'MEDIUM',
            'completion_percentage': 25,
            'total_budget': 120000,
            'spent_amount': 30000,
            'start_date': '2024-03-15',
            'planned_end_date': '2024-12-31',
            'roi_percentage': 0
        },
        {
            'project_code': 'TRN-2024-010',
            'project_name': 'Operations Efficiency Enhancement',
            'department': 'Operations',
            'status': 'IN_PROGRESS',
            'priority': 'HIGH',
            'completion_percentage': 70,
            'total_budget': 80000,
            'spent_amount': 56000,
            'start_date': '2024-02-01',
            'planned_end_date': '2024-10-31',
            'roi_percentage': 24.6
        }
    ]
    
    # Apply filters
    filtered_projects = projects
    
    if status_filter != "All":
        filtered_projects = [p for p in filtered_projects if p['status'] == status_filter]
    
    if dept_filter != "All":
        filtered_projects = [p for p in filtered_projects if p['department'] == dept_filter]
    
    if priority_filter != "All":
        filtered_projects = [p for p in filtered_projects if p['priority'] == priority_filter]
    
    if year_filter != "All":
        filtered_projects = [p for p in filtered_projects if p['start_date'].startswith(year_filter)]
    
    return filtered_projects

# Main dashboard
st.title("🎯 Training Project Status")
st.markdown("Comprehensive tracking of training projects, milestones, and deliverables")

# Filters
col1, col2, col3, col4 = st.columns(4)
with col1:
    status_filter = st.selectbox("Project Status", ["All", "PLANNED", "IN_PROGRESS", "COMPLETED", "ON_HOLD", "CANCELLED"])
with col2:
    dept_filter = st.selectbox("Department", ["All"] + get_departments())
with col3:
    priority_filter = st.selectbox("Priority", ["All", "LOW", "MEDIUM", "HIGH", "CRITICAL"])
with col4:
    year_filter = st.selectbox("Year", ["All", "2024", "2025"])

# Get project data
projects_data = get_projects_data(status_filter, dept_filter, priority_filter, year_filter)

# Project Summary Cards
create_project_summary_cards(projects_data)

st.divider()

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Project Overview", 
    "📈 Progress Tracking", 
    "💰 Budget Analysis", 
    "📅 Timeline & Milestones"
])

with tab1:
    st.subheader("Project Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Project Status Distribution
        status_counts = {}
        for project in projects_data:
            status = project['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            fig_status = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Project Status Distribution",
                color_discrete_map={
                    'PLANNED': '#FFA500',
                    'IN_PROGRESS': '#1f77b4',
                    'COMPLETED': '#2ca02c',
                    'ON_HOLD': '#ff7f0e',
                    'CANCELLED': '#d62728'
                }
            )
            st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Projects by Department
        dept_counts = {}
        for project in projects_data:
            dept = project['department']
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
        
        if dept_counts:
            fig_dept = px.bar(
                x=list(dept_counts.keys()),
                y=list(dept_counts.values()),
                title="Projects by Department",
                labels={'x': 'Department', 'y': 'Number of Projects'}
            )
            fig_dept.update_xaxes(tickangle=45)
            st.plotly_chart(fig_dept, use_container_width=True)
    
    # Detailed project table
    st.subheader("Project Details")
    
    if projects_data:
        project_df = pd.DataFrame([
            {
                'Project Code': project['project_code'],
                'Project Name': project['project_name'],
                'Department': project['department'],
                'Status': project['status'],
                'Priority': project['priority'],
                'Progress (%)': project['completion_percentage'],
                'Budget (KWD)': f"{project['total_budget']:,.0f}",
                'Spent (KWD)': f"{project['spent_amount']:,.0f}",
                'ROI (%)': f"{project.get('roi_percentage', 0):.1f}"
            }
            for project in projects_data
        ])
        
        st.dataframe(project_df, use_container_width=True)
    else:
        st.info("No projects match the selected filters.")

with tab2:
    st.subheader("Project Progress Overview")
    
    if projects_data:
        # Progress by project
        progress_data = []
        for project in projects_data:
            progress_data.append({
                'Project': project['project_name'][:25] + '...' if len(project['project_name']) > 25 else project['project_name'],
                'Progress': project['completion_percentage'],
                'Status': project['status'],
                'Department': project['department']
            })
        
        df_progress = pd.DataFrame(progress_data)
        
        # Progress bar chart
        fig_progress = px.bar(
            df_progress,
            x='Progress',
            y='Project',
            color='Status',
            orientation='h',
            title="Project Completion Progress",
            color_discrete_map={
                'PLANNED': '#FFA500',
                'IN_PROGRESS': '#1f77b4',
                'COMPLETED': '#2ca02c',
                'ON_HOLD': '#ff7f0e',
                'CANCELLED': '#d62728'
            }
        )
        fig_progress.update_layout(height=600)
        st.plotly_chart(fig_progress, use_container_width=True)
    else:
        st.info("No projects to display progress for.")

with tab3:
    st.subheader("Project Budget Analysis")
    
    if projects_data:
        # Budget vs Actual spending
        budget_data = []
        for project in projects_data:
            budget_data.append({
                'Project': project['project_name'][:20] + '...' if len(project['project_name']) > 20 else project['project_name'],
                'Budgeted': project['total_budget'],
                'Spent': project['spent_amount'],
                'Remaining': project['total_budget'] - project['spent_amount']
            })
        
        df_budget = pd.DataFrame(budget_data)
        
        # Budget vs Spent comparison
        fig_budget_comparison = go.Figure()
        
        fig_budget_comparison.add_trace(go.Bar(
            name='Budgeted',
            x=df_budget['Project'],
            y=df_budget['Budgeted'],
            marker_color='lightblue'
        ))
        
        fig_budget_comparison.add_trace(go.Bar(
            name='Spent',
            x=df_budget['Project'],
            y=df_budget['Spent'],
            marker_color='darkblue'
        ))
        
        fig_budget_comparison.update_layout(
            title='Budget vs Actual Spending',
            xaxis_title='Project',
            yaxis_title='Amount (KWD)',
            barmode='group'
        )
        fig_budget_comparison.update_xaxes(tickangle=45)
        st.plotly_chart(fig_budget_comparison, use_container_width=True)
    else:
        st.info("No budget data to display.")

with tab4:
    st.subheader("Project Timeline")
    
    if projects_data:
        # Project timeline table
        timeline_data = []
        for project in projects_data:
            timeline_data.append({
                'Project': project['project_name'],
                'Start Date': project['start_date'],
                'End Date': project['planned_end_date'],
                'Status': project['status'],
                'Progress': f"{project['completion_percentage']}%"
            })
        
        df_timeline = pd.DataFrame(timeline_data)
        st.dataframe(df_timeline, use_container_width=True)
        
        # Project timeline visualization
        st.subheader("Project Timeline Visualization")
        
        # Create Gantt-like chart
        timeline_chart_data = []
        for project in projects_data:
            start_date = datetime.strptime(project['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(project['planned_end_date'], '%Y-%m-%d')
            
            timeline_chart_data.append({
                'Project': project['project_name'][:30] + '...' if len(project['project_name']) > 30 else project['project_name'],
                'Start': start_date,
                'End': end_date,
                'Status': project['status']
            })
        
        df_timeline_chart = pd.DataFrame(timeline_chart_data)
        
        fig_timeline = px.timeline(
            df_timeline_chart,
            x_start='Start',
            x_end='End',
            y='Project',
            color='Status',
            title='Project Timeline Gantt Chart',
            color_discrete_map={
                'PLANNED': '#FFA500',
                'IN_PROGRESS': '#1f77b4',
                'COMPLETED': '#2ca02c',
                'ON_HOLD': '#ff7f0e',
                'CANCELLED': '#d62728'
            }
        )
        fig_timeline.update_layout(height=600)
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("No timeline data to display.")

# Additional insights
st.divider()
st.subheader("📈 Key Insights")

if projects_data:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # High priority projects
        high_priority = [p for p in projects_data if p['priority'] in ['HIGH', 'CRITICAL']]
        st.metric("High Priority Projects", len(high_priority))
        
        if high_priority:
            st.write("**High Priority Projects:**")
            for project in high_priority[:3]:
                st.write(f"• {project['project_name']} ({project['completion_percentage']}%)")
    
    with col2:
        # Budget performance
        over_budget = [p for p in projects_data if p['spent_amount'] > p['total_budget']]
        st.metric("Over Budget Projects", len(over_budget))
        
        if over_budget:
            st.write("**Over Budget Projects:**")
            for project in over_budget[:3]:
                overspend = ((p['spent_amount'] / p['total_budget']) - 1) * 100
                st.write(f"• {project['project_name']} (+{overspend:.1f}%)")
    
    with col3:
        # Completion insights
        near_completion = [p for p in projects_data if p['completion_percentage'] >= 80 and p['status'] != 'COMPLETED']
        st.metric("Near Completion", len(near_completion))
        
        if near_completion:
            st.write("**Near Completion:**")
            for project in near_completion[:3]:
                st.write(f"• {project['project_name']} ({project['completion_percentage']}%)")
else:
    st.info("No data available for insights.")
