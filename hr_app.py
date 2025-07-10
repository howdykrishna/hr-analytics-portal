# hr_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from io import BytesIO
import base64

# Ensure data folder exists (for local testing)
os.makedirs("data", exist_ok=True)

# Page config
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

    # Dataset overview
    st.subheader("📄 Dataset Overview")
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
    st.subheader("📈 Visual Insights")

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

    # Attrition Driver Analysis
    if 'Attrition' in df.columns:
        st.subheader("🔍 What Drives Attrition?")
        df['Attrition_Flag'] = df['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)

        numeric_cols = df.select_dtypes(include=['int64', 'float64']).drop(columns=['Attrition_Flag'], errors='ignore')
        correlations = numeric_cols.corrwith(df['Attrition_Flag']).sort_values(ascending=False)

        st.write("Top correlated factors with Attrition:")
        st.bar_chart(correlations.head(10))

    # Attrition Prediction
    if 'Attrition' in df.columns:
        st.subheader("🔮 Predict Employees At Risk of Leaving")

        df_model = df.copy()
        le = LabelEncoder()
        for col in df_model.select_dtypes(include='object').columns:
            if col != 'Attrition':
                df_model[col] = le.fit_transform(df_model[col])

        X = df_model.drop(columns=['Attrition'])
        y = df_model['Attrition']

        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        df['Attrition_Prob'] = model.predict_proba(X)[:, 1]

        top_risks = df[df['Attrition'] == 'No'].sort_values(by='Attrition_Prob', ascending=False).head(10)
        st.write("Top 10 Employees Likely to Exit:")
        st.dataframe(top_risks[['EmployeeNumber', 'JobRole', 'MonthlyIncome', 'Attrition_Prob']])

        # Download button for top risks
        csv = top_risks.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="attrition_risks.csv">📥 Download At-Risk Employees CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

else:
    st.info("Please upload a CSV or Excel file to begin analysis.")
