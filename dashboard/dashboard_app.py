import sys
import os

#  ABSOLUTE PATH TO PROJECT ROOT
ROOT = r"E:\ecommerce_analytics"
sys.path.append(ROOT)

# dashboard/dashboard_app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from config.config import DB_PATH, CACHE_TTL
import plotly.express as px

st.set_page_config(page_title="E-Commerce Price Dashboard", layout="wide")
st.title("🛍️ Automated E-Commerce Price Intelligence Dashboard")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

@st.cache_data(ttl=CACHE_TTL)
def load_data():
    try:
        df = pd.read_sql("SELECT * FROM product_data", engine)
        if not df.empty and 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error("Error reading DB. Run ETL pipeline first.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.info("No data available. Run `python scripts/etl_pipeline.py` once to populate data.")
else:
    st.sidebar.header("Filters")
    sites = st.sidebar.multiselect("Site/Brand", options=sorted(df['website'].unique()), default=sorted(df['website'].unique()))
    categories = st.sidebar.multiselect("Category", options=sorted(df['category'].dropna().unique()) if 'category' in df.columns else [], default=[])
    keyword = st.sidebar.text_input("Search Product (case-insensitive)", "")

    filtered = df
    if sites:
        filtered = filtered[filtered['website'].isin(sites)]
    if categories:
        filtered = filtered[filtered['category'].isin(categories)]
    if keyword:
        filtered = filtered[filtered['product'].str.contains(keyword, case=False, na=False)]

    st.metric("Records Shown", len(filtered))
    if not filtered.empty:
        st.metric("Average Price", f"₹{filtered['price'].mean():.2f}")
        st.metric("Lowest Price", f"₹{filtered['price'].min():.2f}")

    st.subheader("Recent records")
    st.dataframe(filtered.sort_values("date", ascending=False).head(300))

    st.subheader("Average price by site")
    bar = filtered.groupby('website')['price'].mean().reset_index().sort_values('price')
    fig = px.bar(bar, x='website', y='price', title='Average Price by Site')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Price trend (avg price over time)")
    if not filtered.empty:
        trend = filtered.groupby(filtered['date'].dt.date)['price'].mean().reset_index()
        fig2 = px.line(trend, x='date', y='price', title='Average Price Over Time')
        st.plotly_chart(fig2, use_container_width=True)
