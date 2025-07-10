import plotly.express as px
import streamlit as st

def plot_gender_distribution(df):
    fig = px.pie(df, names='Gender', title='Gender Distribution')
    st.plotly_chart(fig)

def plot_department_distribution(df):
    fig = px.bar(df['Department'].value_counts(), title='Employees by Department')
    st.plotly_chart(fig)

def plot_attrition_by_department(df):
    fig = px.bar(df[df['Attrition'] == 'Yes'], x='Department', title='Attrition by Department')
    st.plotly_chart(fig)

def plot_age_group(df):
    fig = px.histogram(df, x='Age Group', color='Gender', title='Age Group Distribution')
    st.plotly_chart(fig)
