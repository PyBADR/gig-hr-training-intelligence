# GIG HR Training System - Complete Department Structure & Data Generator

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import json

# Complete GIG Department Structure
DEPARTMENTS = [
    # Core Departments
    "Engineering",
    "Sales",
    "Marketing",
    "Human Resources",
    "Finance",
    
    # Additional GIG Departments
    "Legal Department",
    "Information Technology",
    "Corporate Communications",
    "Investor Relations",
    "Marketing & Public Relations",
    
    # HR Sub-departments
    "Talent, Training & Development",
    
    # Finance Related
    "CFO Office",
    "Director of Finance",
    "Accounting",
    
    # Business Units
    "Distribution",
    "Individual Department",
    "Commercial Underwriting",
    "Life & Medical",
    "Corporate Claims",
    "Reinsurance",
    
    # Strategic Units
    "Strategy & Digital Department",
    "Risk Management"
]

# Training Courses Available
TRAINING_COURSES = [
    "AML & Compliance Basics",
    "Insurance Fraud Detection",
    "Advanced Excel for Analysts",
    "Customer Experience Excellence",
    "Underwriting Fundamentals",
    "Claims Management Essentials",
    "Cybersecurity Awareness",
    "Data Analytics for Business",
    "Leadership & Communication",
    "Reinsurance Principles",
    "Risk Assessment Techniques",
    "Digital Transformation",
    "Project Management Professional",
    "Regulatory Compliance",
    "Financial Modeling"
]

def generate_training_data(num_employees=100):
    """Generate synthetic training data for 100 employees"""
    fake = Faker()
    np.random.seed(42)
    random.seed(42)
    
    records = []
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(1, num_employees + 1):
        # Generate employee data
        employee_id = f"EMP{i:04d}"
        employee_name = fake.name()
        department = random.choice(DEPARTMENTS)
        
        # Generate 1-3 training records per employee
        num_trainings = random.randint(1, 3)
        
        for j in range(num_trainings):
            training_course = random.choice(TRAINING_COURSES)
            
            # Random completion date within last year
            completion_date = start_date + timedelta(
                days=random.randint(0, 365)
            )
            
            # Generate score (50-100)
            score = random.randint(50, 100)
            
            # Status based on score
            if score >= 60:
                status = "Completed"
            else:
                status = "In Progress"
            
            records.append({
                "employee_id": employee_id,
                "employee_name": employee_name,
                "department": department,
                "training_course": training_course,
                "completion_date": completion_date.strftime("%Y-%m-%d"),
                "score": score,
                "status": status
            })
    
    return pd.DataFrame(records)

def calculate_department_stats(df):
    """Calculate statistics by department"""
    stats = df.groupby('department').agg({
        'employee_id': 'nunique',
        'score': ['mean', 'min', 'max'],
        'status': lambda x: (x == 'Completed').sum()
    }).round(2)
    
    stats.columns = ['Total_Employees', 'Avg_Score', 'Min_Score', 'Max_Score', 'Completed_Count']
    stats['Completion_Rate'] = (stats['Completed_Count'] / stats['Total_Employees'] * 100).round(1)
    
    return stats

def generate_ml_features(df):
    """Generate features for ML clustering"""
    # Create employee-level aggregated features
    employee_features = df.groupby(['employee_id', 'employee_name', 'department']).agg({
        'score': ['mean', 'min', 'max', 'std'],
        'training_course': 'count',
        'status': lambda x: (x == 'Completed').sum()
    }).reset_index()
    
    employee_features.columns = ['employee_id', 'employee_name', 'department', 
                                 'avg_score', 'min_score', 'max_score', 'std_score',
                                 'total_trainings', 'completed_trainings']
    
    employee_features['completion_rate'] = (
        employee_features['completed_trainings'] / 
        employee_features['total_trainings'] * 100
    ).round(1)
    
    # Fill NaN values in std_score with 0
    employee_features['std_score'] = employee_features['std_score'].fillna(0)
    
    return employee_features

# Generate the data
if __name__ == "__main__":
    # Generate training records
    training_df = generate_training_data(100)
    
    # Calculate department statistics
    dept_stats = calculate_department_stats(training_df)
    
    # Generate ML features
    ml_features = generate_ml_features(training_df)
    
    # Save to files
    training_df.to_csv('training_records.csv', index=False)
    dept_stats.to_csv('department_stats.csv')
    ml_features.to_csv('ml_features.csv', index=False)
    
    # Save departments list as JSON
    with open('departments.json', 'w') as f:
        json.dump(DEPARTMENTS, f, indent=2)
    
    print("✅ Data Generation Complete!")
    print(f"Total Training Records: {len(training_df)}")
    print(f"Unique Employees: {training_df['employee_id'].nunique()}")
    print(f"Departments: {len(DEPARTMENTS)}")
    print("\nDepartment Statistics:")
    print(dept_stats.head())