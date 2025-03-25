# streamlit_app.py

import pandas as pd
import streamlit as st

import altair as alt




st.title("🔍 Athena vs Redshift: COVID-19 Query Comparison")

# Load data (download from S3 or use local for now)
df_athena = pd.read_csv("athena_results.csv")
df_redshift = pd.read_csv("redshift_results.csv")
df_summary = pd.read_csv("comparison_summary.csv")

# Performance table
st.subheader("⏱️ Query Performance Summary")
st.dataframe(df_summary)

# Select location for comparison
location = st.selectbox("Select a Country", sorted(df_redshift['location'].unique()))

# Prepare chart
athena_value = df_athena[df_athena['location'] == location]['avg_new_cases'].values[0]
redshift_value = df_redshift[df_redshift['location'] == location]['avg_new_cases'].values[0]

st.subheader(f"📈 Average New Cases in {location}")
st.bar_chart(pd.DataFrame({
    "source": ["Athena", "Redshift"],
    "avg_new_cases": [athena_value, redshift_value]
}).set_index("source"))
chart = alt.Chart(df_summary).mark_bar().encode(
    x=alt.X('System', sort=None),
    y=alt.Y('Query Time (s)', title='Query Time (seconds)'),
    color='System',
    tooltip=['System', 'Query Time (s)']
).properties(
    title='Athena vs Redshift Query Performance'
)

st.altair_chart(chart, use_container_width=True)