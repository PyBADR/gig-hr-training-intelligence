"""
Real-Time Notifications System
Comprehensive notification management for Gulf Takaful training platform
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="Notifications - Gulf Takaful", page_icon="🔔", layout="wide")

# Initialize session state for notifications
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
    st.session_state.unread_count = 0

def generate_sample_notifications():
    """Generate sample notifications for demonstration"""
    notifications = [
        {
            'id': 1,
            'type': 'deadline',
            'title': 'Training Deadline Approaching',
            'message': 'Compliance Training Module 3 is due in 3 days',
            'timestamp': datetime.now() - timedelta(hours=2),
            'priority': 'high',
            'read': False,
            'category': 'Training',
            'action_required': True
        },
        {
            'id': 2,
            'type': 'achievement',
            'title': 'Certification Earned',
            'message': 'Congratulations! You have earned the Digital Skills Certificate',
            'timestamp': datetime.now() - timedelta(hours=5),
            'priority': 'medium',
            'read': False,
            'category': 'Achievement',
            'action_required': False
        },
        {
            'id': 3,
            'type': 'reminder',
            'title': 'Weekly Training Report',
            'message': 'Your weekly training progress report is ready for review',
            'timestamp': datetime.now() - timedelta(days=1),
            'priority': 'low',
            'read': True,
            'category': 'Report',
            'action_required': False
        },
        {
            'id': 4,
            'type': 'alert',
            'title': 'Budget Alert',
            'message': 'Department training budget is 85% utilized',
            'timestamp': datetime.now() - timedelta(days=2),
            'priority': 'high',
            'read': False,
            'category': 'Budget',
            'action_required': True
        },
        {
            'id': 5,
            'type': 'system',
            'title': 'System Maintenance',
            'message': 'Scheduled maintenance on Sunday 2:00 AM - 4:00 AM',
            'timestamp': datetime.now() - timedelta(days=3),
            'priority': 'medium',
            'read': True,
            'category': 'System',
            'action_required': False
        }
    ]
    return notifications

def get_notification_icon(notification_type):
    """Get icon for notification type"""
    icons = {
        'deadline': '⏰',
        'achievement': '🏆',
        'reminder': '📝',
        'alert': '⚠️',
        'system': '🔧'
    }
    return icons.get(notification_type, '📢')

def get_priority_color(priority):
    """Get color for priority level"""
    colors = {
        'high': '#ff4444',
        'medium': '#ffaa00',
        'low': '#00aa44'
    }
    return colors.get(priority, '#666666')

# Main Dashboard
st.title("🔔 Real-Time Notifications")
st.markdown("Comprehensive notification management and real-time alerts")

# Load sample notifications
if not st.session_state.notifications:
    st.session_state.notifications = generate_sample_notifications()
    st.session_state.unread_count = len([n for n in st.session_state.notifications if not n['read']])

# Notification summary cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_notifications = len(st.session_state.notifications)
    st.metric("Total Notifications", total_notifications)

with col2:
    unread_count = len([n for n in st.session_state.notifications if not n['read']])
    st.metric("Unread", unread_count, delta=f"{unread_count} new")

with col3:
    high_priority = len([n for n in st.session_state.notifications if n['priority'] == 'high'])
    st.metric("High Priority", high_priority)

with col4:
    action_required = len([n for n in st.session_state.notifications if n['action_required']])
    st.metric("Action Required", action_required)

st.divider()

# Notification filters and controls
col1, col2, col3, col4 = st.columns(4)

with col1:
    filter_category = st.selectbox(
        "Filter by Category",
        ["All", "Training", "Achievement", "Report", "Budget", "System"]
    )

with col2:
    filter_priority = st.selectbox(
        "Filter by Priority",
        ["All", "High", "Medium", "Low"]
    )

with col3:
    filter_read = st.selectbox(
        "Filter by Status",
        ["All", "Unread", "Read"]
    )

with col4:
    if st.button("🔄 Refresh Notifications"):
        st.session_state.notifications = generate_sample_notifications()
        st.rerun()

# Filter notifications
filtered_notifications = st.session_state.notifications.copy()

if filter_category != "All":
    filtered_notifications = [n for n in filtered_notifications if n['category'] == filter_category]

if filter_priority != "All":
    filtered_notifications = [n for n in filtered_notifications if n['priority'].title() == filter_priority]

if filter_read == "Unread":
    filtered_notifications = [n for n in filtered_notifications if not n['read']]
elif filter_read == "Read":
    filtered_notifications = [n for n in filtered_notifications if n['read']]

# Sort by timestamp (newest first)
filtered_notifications.sort(key=lambda x: x['timestamp'], reverse=True)

st.divider()

# Notification tabs
tab1, tab2, tab3 = st.tabs(["📋 All Notifications", "📊 Analytics", "⚙️ Settings"])

with tab1:
    st.subheader(f"Notifications ({len(filtered_notifications)})")
    
    if filtered_notifications:
        for notification in filtered_notifications:
            with st.container():
                col1, col2, col3 = st.columns([1, 8, 1])
                
                with col1:
                    icon = get_notification_icon(notification['type'])
                    st.markdown(f"<div style='font-size: 24px; text-align: center;'>{icon}</div>", unsafe_allow_html=True)
                
                with col2:
                    # Notification header
                    priority_color = get_priority_color(notification['priority'])
                    read_status = "" if notification['read'] else "🔴 "
                    
                    st.markdown(f"""
                    <div style="border-left: 4px solid {priority_color}; padding-left: 10px; margin-bottom: 5px;">
                        <h4 style="margin: 0; color: {priority_color};">{read_status}{notification['title']}</h4>
                        <p style="margin: 5px 0; color: #666;">{notification['message']}</p>
                        <small style="color: #999;">
                            {notification['timestamp'].strftime('%Y-%m-%d %H:%M')} • 
                            {notification['category']} • 
                            Priority: {notification['priority'].title()}
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if notification['action_required']:
                        st.warning("⚡ Action Required")
                
                with col3:
                    if not notification['read']:
                        if st.button("✓", key=f"mark_read_{notification['id']}", help="Mark as read"):
                            notification['read'] = True
                            st.rerun()
                
                st.divider()
    else:
        st.info("No notifications match the selected filters.")

with tab2:
    st.subheader("📊 Notification Analytics")
    
    # Create analytics charts
    notifications_df = pd.DataFrame(st.session_state.notifications)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Notifications by category
        category_counts = notifications_df['category'].value_counts()
        fig_category = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Notifications by Category"
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        # Notifications by priority
        priority_counts = notifications_df['priority'].value_counts()
        fig_priority = px.bar(
            x=priority_counts.index,
            y=priority_counts.values,
            title="Notifications by Priority",
            color=priority_counts.index,
            color_discrete_map={'high': '#ff4444', 'medium': '#ffaa00', 'low': '#00aa44'}
        )
        st.plotly_chart(fig_priority, use_container_width=True)
    
    # Notification timeline
    st.subheader("📈 Notification Timeline")
    
    # Group by date
    notifications_df['date'] = pd.to_datetime(notifications_df['timestamp']).dt.date
    daily_counts = notifications_df.groupby('date').size().reset_index()
    daily_counts.columns = ['Date', 'Count']
    
    fig_timeline = px.line(
        daily_counts,
        x='Date',
        y='Count',
        title='Daily Notification Volume',
        markers=True
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

with tab3:
    st.subheader("⚙️ Notification Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📧 Email Notifications")
        
        email_training = st.checkbox("Training deadlines", value=True)
        email_achievements = st.checkbox("Achievements and certifications", value=True)
        email_budget = st.checkbox("Budget alerts", value=True)
        email_system = st.checkbox("System maintenance", value=False)
        
        st.markdown("### 📱 Push Notifications")
        
        push_urgent = st.checkbox("Urgent alerts only", value=True)
        push_all = st.checkbox("All notifications", value=False)
        
        st.markdown("### ⏰ Notification Timing")
        
        notification_hours = st.slider(
            "Active hours (24h format)",
            min_value=0,
            max_value=23,
            value=(8, 18),
            help="Notifications will only be sent during these hours"
        )
    
    with col2:
        st.markdown("### 🔔 Notification Types")
        
        # Notification type preferences
        types_config = {
            "Training Deadlines": {"enabled": True, "advance_days": 3},
            "Budget Alerts": {"enabled": True, "threshold": 80},
            "Achievement Notifications": {"enabled": True, "immediate": True},
            "System Updates": {"enabled": False, "advance_hours": 24},
            "Weekly Reports": {"enabled": True, "day": "Monday"}
        }
        
        for notification_type, config in types_config.items():
            with st.expander(f"⚙️ {notification_type}"):
                enabled = st.checkbox(f"Enable {notification_type}", value=config['enabled'])
                
                if notification_type == "Training Deadlines" and enabled:
                    st.slider("Advance notice (days)", 1, 7, config['advance_days'])
                elif notification_type == "Budget Alerts" and enabled:
                    st.slider("Alert threshold (%)", 50, 100, config['threshold'])
                elif notification_type == "System Updates" and enabled:
                    st.slider("Advance notice (hours)", 1, 48, config['advance_hours'])
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Notification settings saved successfully!")

# Real-time notification simulation
st.divider()
st.subheader("🔄 Real-Time Simulation")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Simulate New Notifications:**")
    
    if st.button("📚 Training Reminder"):
        new_notification = {
            'id': len(st.session_state.notifications) + 1,
            'type': 'reminder',
            'title': 'New Training Available',
            'message': 'Leadership Development Course is now available for enrollment',
            'timestamp': datetime.now(),
            'priority': 'medium',
            'read': False,
            'category': 'Training',
            'action_required': True
        }
        st.session_state.notifications.insert(0, new_notification)
        st.success("📚 Training reminder added!")
        st.rerun()
    
    if st.button("⚠️ Budget Alert"):
        new_notification = {
            'id': len(st.session_state.notifications) + 1,
            'type': 'alert',
            'title': 'Budget Threshold Exceeded',
            'message': 'IT Department has exceeded 90% of training budget',
            'timestamp': datetime.now(),
            'priority': 'high',
            'read': False,
            'category': 'Budget',
            'action_required': True
        }
        st.session_state.notifications.insert(0, new_notification)
        st.error("⚠️ Budget alert added!")
        st.rerun()

with col2:
    st.markdown("**Bulk Actions:**")
    
    if st.button("✅ Mark All as Read"):
        for notification in st.session_state.notifications:
            notification['read'] = True
        st.success("All notifications marked as read!")
        st.rerun()
    
    if st.button("🗑️ Clear Read Notifications"):
        st.session_state.notifications = [n for n in st.session_state.notifications if not n['read']]
        st.success("Read notifications cleared!")
        st.rerun()

# Footer with notification statistics
st.divider()
st.markdown("### 📊 Notification Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_daily = len(st.session_state.notifications) / 7  # Assuming 7 days of data
    st.metric("Avg Daily", f"{avg_daily:.1f}")

with col2:
    response_time = "2.3 min"  # Mock data
    st.metric("Avg Response Time", response_time)

with col3:
    read_rate = len([n for n in st.session_state.notifications if n['read']]) / len(st.session_state.notifications) * 100
    st.metric("Read Rate", f"{read_rate:.1f}%")

with col4:
    action_rate = 85  # Mock data
    st.metric("Action Completion", f"{action_rate}%")

# Auto-refresh notice
st.info("🔄 This page automatically refreshes every 30 seconds to show new notifications in a real deployment.")
