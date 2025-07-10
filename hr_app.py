# hr_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Ensure data folder exists (for local testing)
os.makedirs("data", exist_ok=True)

# Title
st.set_page_config(page_title="HR Analytics Portal", layout="wide")
st.title("📊 HR Analytics Dashboard")

# Upload File
uploaded_file = st.file_uploader("Upload HR Data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]

    if file_type == 'csv':
        df = pd.read_csv(uploaded_file)
    elif file_type == 'xlsx':
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    else:
        st.error("Unsupported file format")
        st.stop()

    # Optional: Save for local development
    with open(f"data/uploaded_file.{file_type}", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Basic info
    st.subheader("Dataset Overview")
    st.write(df.head())
    st.markdown(f"**Total Records:** {len(df)}")

    # Sidebar filters
    st.sidebar.header("Filters")
    if 'Department' in df.columns:
        departments = st.sidebar.multiselect("Select Departments", df['Department'].unique(), default=df['Department'].unique())
        df = df[df['Department'].isin(departments)]

    # Summary KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Headcount", len(df))
    if 'Age' in df.columns:
        col2.metric("🧓 Average Age", round(df['Age'].mean(), 1))
    if 'MonthlyIncome' in df.columns:
        col3.metric("💰 Avg. Monthly Income", f"${int(df['MonthlyIncome'].mean())}")

    # Charts
    st.subheader("Visual Insights")

    if 'Department' in df.columns:
        fig_dept = px.histogram(df, x='Department', title="Employees by Department")
        st.plotly_chart(fig_dept, use_container_width=True)

    if 'JobRole' in df.columns:
        fig_role = px.histogram(df, x='JobRole', title="Employees by Job Role")
        st.plotly_chart(fig_role, use_container_width=True)

    if 'Gender' in df.columns:
        fig_gender = px.pie(df, names='Gender', title="Gender Distribution")
        st.plotly_chart(fig_gender, use_container_width=True)

    if 'Attrition' in df.columns:
        fig_attrition = px.histogram(df, x='Department', color='Attrition', barmode='group', title="Attrition by Department")
        st.plotly_chart(fig_attrition, use_container_width=True)

    if 'MonthlyIncome' in df.columns and 'JobRole' in df.columns:
        fig_income = px.box(df, x='JobRole', y='MonthlyIncome', title="Income Distribution by Role")
        st.plotly_chart(fig_income, use_container_width=True)

else:
    st.info("Please upload a CSV or Excel file to begin analysis.")
