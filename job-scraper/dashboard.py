import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.title("Job Listings Scraper & Analyzer")

keyword = st.text_input("Enter job keyword: ", "python")

if st.button("Scrape Jobs"):
    response = requests.post(f"{API_URL}/scrape/{keyword}")

    if response.status_code == 200:
        data = response.json()
        scraped_count = data.get("scraped_jobs", 0)
        st.success(f"Scraped {scraped_count} jobs!")
    else:
        st.error(f"Error: {response.status_code}")
        st.write(response.text)

# Fetch jobs
response = requests.get(f"{API_URL}/jobs")

if response.status_code == 200:
    data = response.json()

    if data:
        df = pd.DataFrame(data)

        st.subheader("Job Listings")
        st.dataframe(df)

        st.subheader("Jobs by Keyword")
        fig1 = px.histogram(df, x="keyword")
        st.plotly_chart(fig1)

        st.subheader("Top Hiring Companies")
        top_companies = df["company"].value_counts().reset_index()
        top_companies.columns = ["company", "count"]

        fig2 = px.bar(top_companies.head(10), x="company", y="count")
        st.plotly_chart(fig2)
    else:
        st.info("No jobs in database yet. Run the scraper!")