"""
Mobile-Responsive Design Demo
Demonstration of mobile-optimized features for Gulf Takaful training platform
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent.parent / 'app'
sys.path.append(str(app_dir))

try:
    from utils.mobile_utils import (
        inject_mobile_css,
        create_mobile_friendly_metrics,
        create_responsive_chart_config,
        create_responsive_layout,
        create_mobile_friendly_table,
        create_touch_friendly_filters,
        add_mobile_download_button,
        optimize_for_mobile
    )
except ImportError:
    st.error("Could not import mobile utilities. Please ensure the utils directory is properly set up.")
    st.stop()

st.set_page_config(
    page_title="Mobile Demo - Gulf Takaful", 
    page_icon="📱", 
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with sidebar collapsed for mobile
)

# Apply mobile optimizations
@optimize_for_mobile
def main():
    """Main mobile demo function"""
    
    # Mobile-friendly header
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, #1f4e79 0%, #2c5aa0 100%); color: white; border-radius: 10px; margin-bottom: 1rem;">
        <h1 style="margin: 0; font-size: 1.5rem;">📱 Mobile-Responsive Demo</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Gulf Takaful Training Platform - Optimized for Mobile</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Device info section
    st.subheader("📱 Device Optimization Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **✅ Mobile Features:**
        - Responsive layout design
        - Touch-friendly buttons
        - Optimized chart sizing
        - Collapsible sidebar
        - Swipe-friendly tabs
        - Large touch targets
        """)
    
    with col2:
        st.markdown("""
        **💻 Desktop Features:**
        - Full sidebar navigation
        - Hover interactions
        - Larger chart displays
        - Multi-column layouts
        - Keyboard shortcuts
        - Advanced tooltips
        """)
    
    st.divider()
    
    # Mobile-friendly metrics demonstration
    st.subheader("📊 Mobile-Optimized Metrics")
    
    # Sample metrics data
    metrics_data = [
        {'label': 'Total Employees', 'value': '3,247', 'delta': '+127', 'help': 'Total active employees'},
        {'label': 'Training Completion', 'value': '87.3%', 'delta': '+5.2%', 'help': 'Overall completion rate'},
        {'label': 'Budget Utilization', 'value': '78.5%', 'delta': '-2.1%', 'help': 'Budget spent vs allocated'},
        {'label': 'Satisfaction Score', 'value': '4.2/5.0', 'delta': '+0.3', 'help': 'Average employee satisfaction'}
    ]
    
    create_mobile_friendly_metrics(metrics_data, columns=2)
    
    st.divider()
    
    # Touch-friendly filters demonstration
    st.subheader("🔍 Touch-Friendly Filters")
    
    filter_config = [
        {
            'type': 'selectbox',
            'key': 'department_filter',
            'label': 'Department',
            'options': ['All', 'IT', 'HR', 'Finance', 'Operations', 'Claims'],
            'default': 'All'
        },
        {
            'type': 'selectbox',
            'key': 'period_filter',
            'label': 'Time Period',
            'options': ['Last 30 Days', 'Last Quarter', 'Last 6 Months', 'Last Year'],
            'default': 'Last Quarter'
        }
    ]
    
    filters = create_touch_friendly_filters(filter_config)
    
    st.divider()
    
    # Responsive charts demonstration
    st.subheader("📈 Responsive Charts")
    
    # Create sample data
    departments = ['IT', 'HR', 'Finance', 'Operations', 'Claims', 'Underwriting']
    training_data = {
        'Department': departments,
        'Completed': np.random.randint(50, 100, len(departments)),
        'In Progress': np.random.randint(10, 30, len(departments)),
        'Planned': np.random.randint(5, 20, len(departments))
    }
    
    df = pd.DataFrame(training_data)
    
    # Mobile-optimized chart tabs
    tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "🍰 Pie Chart", "📈 Line Chart"])
    
    with tab1:
        # Responsive bar chart
        fig_bar = px.bar(
            df, 
            x='Department', 
            y=['Completed', 'In Progress', 'Planned'],
            title='Training Status by Department',
            barmode='stack'
        )
        
        # Apply mobile-responsive layout
        fig_bar.update_layout(
            **create_responsive_layout({
                'title': {'font': {'size': 14}},
                'xaxis': {'tickangle': 45}
            })
        )
        
        st.plotly_chart(
            fig_bar, 
            use_container_width=True, 
            config=create_responsive_chart_config()
        )
    
    with tab2:
        # Responsive pie chart
        total_completed = df['Completed'].sum()
        total_in_progress = df['In Progress'].sum()
        total_planned = df['Planned'].sum()
        
        fig_pie = px.pie(
            values=[total_completed, total_in_progress, total_planned],
            names=['Completed', 'In Progress', 'Planned'],
            title='Overall Training Distribution'
        )
        
        fig_pie.update_layout(
            **create_responsive_layout({
                'title': {'font': {'size': 14}}
            })
        )
        
        st.plotly_chart(
            fig_pie, 
            use_container_width=True, 
            config=create_responsive_chart_config()
        )
    
    with tab3:
        # Responsive line chart with time series data
        dates = pd.date_range(start='2024-01-01', end='2024-09-11', freq='W')
        completion_rates = np.random.uniform(75, 95, len(dates))
        
        fig_line = px.line(
            x=dates,
            y=completion_rates,
            title='Training Completion Rate Trend',
            labels={'x': 'Date', 'y': 'Completion Rate (%)'}
        )
        
        fig_line.update_layout(
            **create_responsive_layout({
                'title': {'font': {'size': 14}},
                'xaxis': {'tickangle': 45}
            })
        )
        
        st.plotly_chart(
            fig_line, 
            use_container_width=True, 
            config=create_responsive_chart_config()
        )
    
    st.divider()
    
    # Mobile-friendly table demonstration
    st.subheader("📋 Mobile-Optimized Data Table")
    
    # Generate sample employee data
    sample_employees = []
    for i in range(25):
        sample_employees.append({
            'ID': f'EMP{i+1:03d}',
            'Name': f'Employee {i+1}',
            'Department': np.random.choice(departments),
            'Completion Rate': f"{np.random.uniform(70, 100):.1f}%",
            'Training Hours': np.random.randint(20, 80),
            'Last Training': (datetime.now() - timedelta(days=np.random.randint(1, 90))).strftime('%Y-%m-%d'),
            'Status': np.random.choice(['Active', 'On Leave', 'Training'])
        })
    
    employees_df = pd.DataFrame(sample_employees)
    
    # Apply department filter
    if filters['department_filter'] != 'All':
        employees_df = employees_df[employees_df['Department'] == filters['department_filter']]
    
    create_mobile_friendly_table(employees_df, max_rows=8)
    
    st.divider()
    
    # Mobile download demonstration
    st.subheader("📥 Mobile-Friendly Downloads")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV download
        csv_data = employees_df.to_csv(index=False)
        add_mobile_download_button(
            data=csv_data,
            filename=f"employee_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime_type="text/csv",
            label="Download Employee Data (CSV)"
        )
    
    with col2:
        # JSON download
        json_data = employees_df.to_json(orient='records', indent=2)
        add_mobile_download_button(
            data=json_data,
            filename=f"employee_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime_type="application/json",
            label="Download Employee Data (JSON)"
        )
    
    st.divider()
    
    # Mobile interaction examples
    st.subheader("👆 Touch Interactions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Touch-Friendly Buttons:**")
        
        if st.button("🚀 Large Action Button", use_container_width=True):
            st.success("Button pressed! Touch interaction successful.")
        
        if st.button("📈 View Analytics", use_container_width=True):
            st.info("Analytics view would open here.")
        
        if st.button("⚙️ Settings", use_container_width=True):
            st.warning("Settings panel would appear here.")
    
    with col2:
        st.markdown("**Touch-Friendly Inputs:**")
        
        # Large touch targets for inputs
        user_rating = st.slider(
            "Rate your mobile experience",
            min_value=1,
            max_value=5,
            value=4,
            help="Drag to rate the mobile interface"
        )
        
        feedback = st.text_area(
            "Mobile feedback",
            placeholder="How is the mobile experience?",
            height=100
        )
        
        if st.button("Submit Feedback", use_container_width=True):
            st.success(f"Thank you! Rating: {user_rating}/5")
    
    st.divider()
    
    # Progressive Web App features
    st.subheader("📱 Progressive Web App Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📲 Install App**
        - Add to home screen
        - Offline functionality
        - Native app feel
        """)
    
    with col2:
        st.markdown("""
        **🔔 Push Notifications**
        - Training reminders
        - Deadline alerts
        - Achievement notifications
        """)
    
    with col3:
        st.markdown("""
        **📶 Offline Support**
        - Cached data viewing
        - Sync when online
        - Background updates
        """)
    
    # PWA installation prompt (placeholder)
    if st.button("📲 Install Gulf Takaful Training App", use_container_width=True):
        st.info("📱 Installation prompt would appear here. Add this app to your home screen for the best mobile experience!")
    
    st.divider()
    
    # Mobile performance metrics
    st.subheader("⚡ Mobile Performance")
    
    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
    
    with perf_col1:
        st.metric("Load Time", "1.2s", "-0.3s")
    
    with perf_col2:
        st.metric("Bundle Size", "245KB", "-15KB")
    
    with perf_col3:
        st.metric("Mobile Score", "94/100", "+8")
    
    with perf_col4:
        st.metric("Touch Response", "<50ms", "Excellent")
    
    # Footer with mobile tips
    st.divider()
    st.markdown("""
    **💡 Mobile Usage Tips:**
    - Rotate device for better chart viewing
    - Use pinch-to-zoom on charts for details
    - Swipe left/right on tabs for navigation
    - Long press on buttons for additional options
    - Pull down to refresh data
    """)
    
    # Device detection info (placeholder)
    st.info("""
    📱 **Device Detection:** This demo shows mobile-optimized features. 
    The actual app would detect your device type and automatically apply the best layout.
    """)

if __name__ == "__main__":
    main()
