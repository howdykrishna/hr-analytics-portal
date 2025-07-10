import pandas as pd

def process_data(file_path):
    df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    df['Age Group'] = pd.cut(df['Age'], bins=[18, 25, 35, 45, 60], labels=['18-25', '26-35', '36-45', '46-60'])
    return df

def generate_summary(df):
    return {
        "Total Employees": len(df),
        "Average Age": int(df['Age'].mean()),
        "Gender Distribution": df['Gender'].value_counts(),
        "Department Count": df['Department'].value_counts(),
        "Attrition Rate": df['Attrition'].value_counts(normalize=True).get('Yes', 0) * 100
    }
