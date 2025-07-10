import streamlit as st
from utils import save_file, get_uploaded_file
from data_processor import process_data, generate_summary
import visualizations as viz
import os

st.set_page_config(page_title="HR Analytics Portal", layout="wide")
st.title("📊 HR Analytics Dashboard")

uploaded_file = st.file_uploader("Upload HR Excel/CSV File", type=["xlsx", "csv"])
if uploaded_file:
    save_file(uploaded_file)
    st.success("File uploaded successfully!")

file_path = get_uploaded_file()

if file_path:
    df = process_data(file_path)
    summary = generate_summary(df)

    # KPIs
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Employees", summary["Total Employees"])
    col2.metric("Average Age", summary["Average Age"])
    col3.metric("Attrition Rate", f'{summary["Attrition Rate"]:.2f}%')
    col4.metric("Departments", len(summary["Department Count"]))

    st.markdown("---")

    # Charts
    viz.plot_gender_distribution(df)
    viz.plot_age_group(df)
    viz.plot_department_distribution(df)
    viz.plot_attrition_by_department(df)
else:
    st.warning("Please upload a file to begin analysis.")
