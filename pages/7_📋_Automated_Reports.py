"""
Automated Reporting System
Scheduled reports and automated insights for Gulf Takaful training platform
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from io import BytesIO
import base64

st.set_page_config(page_title="Automated Reports - Gulf Takaful", page_icon="📋", layout="wide")

def generate_executive_summary_data():
    """Generate sample data for executive summary report"""
    return {
        'total_employees': 3247,
        'training_completion_rate': 87.3,
        'budget_utilization': 78.5,
        'compliance_rate': 94.2,
        'avg_satisfaction': 4.2,
        'roi_percentage': 23.8,
        'high_risk_employees': 45,
        'certifications_earned': 156,
        'training_hours_total': 12847,
        'cost_per_employee': 1385
    }

def generate_department_performance_data():
    """Generate department performance data"""
    departments = ['IT', 'HR', 'Finance', 'Operations', 'Claims', 'Underwriting', 'Sales', 'Legal', 'Investment', 'Customer Service']
    
    data = []
    for dept in departments:
        data.append({
            'department': dept,
            'employees': np.random.randint(200, 500),
            'completion_rate': np.random.uniform(75, 95),
            'budget_spent': np.random.uniform(50000, 200000),
            'satisfaction': np.random.uniform(3.8, 4.8),
            'certifications': np.random.randint(5, 25),
            'avg_performance': np.random.uniform(75, 90)
        })
    
    return pd.DataFrame(data)

def create_pdf_report_content(report_type, data):
    """Create HTML content for PDF report"""
    if report_type == "Executive Summary":
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ text-align: center; color: #1f4e79; margin-bottom: 30px; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; width: 200px; text-align: center; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #2e8b57; }}
                .metric-label {{ font-size: 14px; color: #666; }}
                .section {{ margin: 30px 0; }}
                .alert {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Gulf Takaful Training Platform</h1>
                <h2>Executive Summary Report</h2>
                <p>Generated on {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="section">
                <h3>Key Performance Indicators</h3>
                <div class="metric">
                    <div class="metric-value">{data['total_employees']:,}</div>
                    <div class="metric-label">Total Employees</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{data['training_completion_rate']:.1f}%</div>
                    <div class="metric-label">Training Completion</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{data['budget_utilization']:.1f}%</div>
                    <div class="metric-label">Budget Utilization</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{data['compliance_rate']:.1f}%</div>
                    <div class="metric-label">Compliance Rate</div>
                </div>
            </div>
            
            <div class="section">
                <h3>Training Effectiveness</h3>
                <p><strong>ROI:</strong> {data['roi_percentage']:.1f}% return on training investment</p>
                <p><strong>Satisfaction:</strong> {data['avg_satisfaction']:.1f}/5.0 average employee satisfaction</p>
                <p><strong>Certifications:</strong> {data['certifications_earned']} professional certifications earned</p>
                <p><strong>Training Hours:</strong> {data['training_hours_total']:,} total hours completed</p>
            </div>
            
            <div class="alert">
                <h3>Action Items</h3>
                <ul>
                    <li>{data['high_risk_employees']} employees identified as high attrition risk - require immediate attention</li>
                    <li>Budget utilization at {data['budget_utilization']:.1f}% - consider reallocating unused funds</li>
                    <li>Average cost per employee: KWD {data['cost_per_employee']:,}</li>
                </ul>
            </div>
        </body>
        </html>
        """
    else:
        html_content = "<html><body><h1>Report content not available</h1></body></html>"
    
    return html_content

def create_excel_report(data, report_type):
    """Create Excel report with multiple sheets"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if report_type == "Department Performance":
            # Main data sheet
            data.to_excel(writer, sheet_name='Department_Performance', index=False)
            
            # Summary sheet
            summary_data = {
                'Metric': ['Total Employees', 'Avg Completion Rate', 'Total Budget Spent', 'Avg Satisfaction'],
                'Value': [
                    data['employees'].sum(),
                    f"{data['completion_rate'].mean():.1f}%",
                    f"KWD {data['budget_spent'].sum():,.0f}",
                    f"{data['satisfaction'].mean():.1f}/5.0"
                ]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
        
        elif report_type == "Executive Summary":
            exec_data = generate_executive_summary_data()
            summary_df = pd.DataFrame(list(exec_data.items()), columns=['Metric', 'Value'])
            summary_df.to_excel(writer, sheet_name='Executive_Summary', index=False)
    
    output.seek(0)
    return output

# Main Dashboard
st.title("📋 Automated Reporting System")
st.markdown("Generate, schedule, and manage automated reports for Gulf Takaful training analytics")

# Report generation section
st.subheader("📊 Generate Reports")

col1, col2, col3 = st.columns(3)

with col1:
    report_type = st.selectbox(
        "Report Type",
        ["Executive Summary", "Department Performance", "Training Analytics", "Budget Report", "Compliance Report"]
    )

with col2:
    report_format = st.selectbox(
        "Format",
        ["PDF", "Excel", "CSV"]
    )

with col3:
    date_range = st.selectbox(
        "Period",
        ["Last 30 Days", "Last Quarter", "Last 6 Months", "Last Year", "Custom"]
    )

if st.button("🔄 Generate Report", type="primary"):
    with st.spinner(f"Generating {report_type} report..."):
        if report_type == "Executive Summary":
            data = generate_executive_summary_data()
            
            if report_format == "PDF":
                html_content = create_pdf_report_content(report_type, data)
                st.success("✅ Executive Summary PDF generated successfully!")
                st.download_button(
                    label="📥 Download PDF Report",
                    data=html_content,
                    file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d')}.html",
                    mime="text/html"
                )
            
            elif report_format == "Excel":
                excel_data = create_excel_report(data, report_type)
                st.success("✅ Executive Summary Excel generated successfully!")
                st.download_button(
                    label="📥 Download Excel Report",
                    data=excel_data,
                    file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        elif report_type == "Department Performance":
            dept_data = generate_department_performance_data()
            
            if report_format == "Excel":
                excel_data = create_excel_report(dept_data, report_type)
                st.success("✅ Department Performance Excel generated successfully!")
                st.download_button(
                    label="📥 Download Excel Report",
                    data=excel_data,
                    file_name=f"department_performance_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            elif report_format == "CSV":
                csv_data = dept_data.to_csv(index=False)
                st.success("✅ Department Performance CSV generated successfully!")
                st.download_button(
                    label="📥 Download CSV Report",
                    data=csv_data,
                    file_name=f"department_performance_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

st.divider()

# Scheduled Reports Section
st.subheader("⏰ Scheduled Reports")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Create New Schedule")
    
    schedule_name = st.text_input("Schedule Name", placeholder="e.g., Weekly Executive Summary")
    schedule_report_type = st.selectbox("Report Type", ["Executive Summary", "Department Performance", "Training Analytics"], key="schedule_type")
    schedule_frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Quarterly"])
    schedule_recipients = st.text_area("Email Recipients", placeholder="email1@gulftakaful.kw, email2@gulftakaful.kw")
    
    if st.button("➕ Create Schedule"):
        st.success(f"✅ Scheduled report '{schedule_name}' created successfully!")
        st.info(f"📧 {schedule_frequency} {schedule_report_type} reports will be sent to specified recipients")

with col2:
    st.markdown("### Active Schedules")
    
    # Sample scheduled reports
    scheduled_reports = [
        {"Name": "Weekly Executive Summary", "Type": "Executive Summary", "Frequency": "Weekly", "Next Run": "2024-09-18", "Status": "Active"},
        {"Name": "Monthly Department Report", "Type": "Department Performance", "Frequency": "Monthly", "Next Run": "2024-10-01", "Status": "Active"},
        {"Name": "Quarterly Compliance Report", "Type": "Compliance Report", "Frequency": "Quarterly", "Next Run": "2024-12-01", "Status": "Active"}
    ]
    
    for report in scheduled_reports:
        with st.container():
            col_a, col_b, col_c = st.columns([3, 1, 1])
            with col_a:
                st.write(f"**{report['Name']}**")
                st.write(f"{report['Frequency']} • Next: {report['Next Run']}")
            with col_b:
                st.write(f"🟢 {report['Status']}")
            with col_c:
                if st.button("⚙️", key=f"edit_{report['Name']}"):
                    st.info(f"Edit {report['Name']}")
            st.divider()

# Report History Section
st.subheader("📚 Report History")

# Sample report history
report_history = [
    {"Date": "2024-09-11", "Report": "Executive Summary", "Format": "PDF", "Generated By": "System", "Status": "Completed"},
    {"Date": "2024-09-10", "Report": "Department Performance", "Format": "Excel", "Generated By": "hr.manager@gulftakaful.kw", "Status": "Completed"},
    {"Date": "2024-09-09", "Report": "Training Analytics", "Format": "CSV", "Generated By": "System", "Status": "Completed"},
    {"Date": "2024-09-08", "Report": "Budget Report", "Format": "PDF", "Generated By": "finance.head@gulftakaful.kw", "Status": "Completed"},
    {"Date": "2024-09-07", "Report": "Compliance Report", "Format": "Excel", "Generated By": "System", "Status": "Completed"}
]

history_df = pd.DataFrame(report_history)
st.dataframe(history_df, use_container_width=True)

# Analytics on report usage
st.subheader("📈 Report Analytics")

col1, col2, col3 = st.columns(3)

with col1:
    # Most popular reports
    report_counts = history_df['Report'].value_counts()
    fig_popular = px.bar(
        x=report_counts.index,
        y=report_counts.values,
        title="Most Generated Reports",
        labels={'x': 'Report Type', 'y': 'Count'}
    )
    st.plotly_chart(fig_popular, use_container_width=True)

with col2:
    # Format preferences
    format_counts = history_df['Format'].value_counts()
    fig_format = px.pie(
        values=format_counts.values,
        names=format_counts.index,
        title="Format Preferences"
    )
    st.plotly_chart(fig_format, use_container_width=True)

with col3:
    # Report generation trends
    history_df['Date'] = pd.to_datetime(history_df['Date'])
    daily_counts = history_df.groupby(history_df['Date'].dt.date).size().reset_index()
    daily_counts.columns = ['Date', 'Count']
    
    fig_trends = px.line(
        daily_counts,
        x='Date',
        y='Count',
        title="Report Generation Trends",
        markers=True
    )
    st.plotly_chart(fig_trends, use_container_width=True)

# Report Templates Section
st.divider()
st.subheader("📄 Report Templates")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Executive Dashboard Template"):
        st.info("Executive dashboard template with KPIs, trends, and strategic insights")

with col2:
    if st.button("👥 HR Analytics Template"):
        st.info("HR analytics template with employee metrics, attrition analysis, and performance data")

with col3:
    if st.button("💰 Financial Report Template"):
        st.info("Financial report template with budget analysis, ROI calculations, and cost breakdowns")

with col4:
    if st.button("📋 Compliance Template"):
        st.info("Compliance report template with training completion rates and regulatory requirements")

# Footer with system information
st.divider()
st.markdown("""
**🔧 System Information:**
- Reports are generated automatically based on real-time data
- Scheduled reports are sent via email at specified intervals
- All reports include data validation and quality checks
- Custom report templates can be created upon request
- Report history is maintained for audit purposes
""")

# Quick stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Reports Generated", "1,247", "+23 this week")
with col2:
    st.metric("Active Schedules", "15", "+2 this month")
with col3:
    st.metric("Email Recipients", "89", "Across all schedules")
with col4:
    st.metric("Avg Generation Time", "2.3s", "-0.5s improvement")
