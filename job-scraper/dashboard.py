# Note to me: Save job still doesn't work, look forward to fixing

import streamlit as st
import requests
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Job Scraper Pro",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.sidebar.title("Job Scraper Pro")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Job Explorer", "My Jobs", "Analytics"]
)

# Auth
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Login/Signup
if not st.session_state.logged_in:

    st.title("Login or Register")

    auth_option = st.radio("Choose option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(auth_option):

        endpoint = "/login" if auth_option == "Login" else "/register"

        response = requests.post(
            f"{API_URL}{endpoint}",
            json={"username": username, "password": password}
        )

        if response.status_code != 200:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)
            st.stop()

        data = response.json()

        if "error" in data:
            st.error(data["error"])
        else:
            st.success(data.get("message", "Success"))

            if auth_option == "Login":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()

    st.stop()

st.sidebar.success(f"Logged in as: {st.session_state.username}")


# Fetch data
jobs_response = requests.get(f"{API_URL}/jobs")

if jobs_response.status_code != 200:
    st.error("Failed to fetch jobs")
    st.write(jobs_response.text)
    st.stop()

jobs_data = jobs_response.json()
df = pd.DataFrame(jobs_data) if jobs_data else pd.DataFrame()

my_jobs_response = requests.get(
    f"{API_URL}/my-jobs/{st.session_state.username}"
)

if my_jobs_response.status_code == 200:
    my_df = pd.DataFrame(my_jobs_response.json())
else:
    my_df = pd.DataFrame()


# Dashboard
if page == "Dashboard":

    st.title("Job Market Overview")

    if df.empty:
        st.info("No jobs available.")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Jobs", len(df))
        col2.metric("Saved Jobs", len(my_df))
        col3.metric("Unique Companies", df["company"].nunique())

        st.divider()

        keyword = st.text_input("Scrape new keyword:", "python")

        if st.button("Scrape Jobs"):
            r = requests.post(f"{API_URL}/scrape/{keyword}")
            if r.status_code == 200:
                st.success("Scrape complete!")
                st.rerun()
            else:
                st.error(r.text)


# Job Explorer
elif page == "Job Explorer":

    st.title("Explore Jobs")

    if df.empty:
        st.info("No jobs found.")
    else:
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.subheader("Save Job")

        # Detect correct ID column automatically
        if "id" in df.columns:
            id_column = "id"
        elif "job_id" in df.columns:
            id_column = "job_id"
        else:
            st.error("No valid job ID column found.")
            st.stop()

        selected_job = st.selectbox(
            "Select job to save",
            df["title"]
        )

        if st.button("Save to My Jobs"):

            payload = {
                "username": st.session_state.username,
                "job_id": selected_job
            }

            save_response = requests.post(
                f"{API_URL}/save-job",
                json=payload
            )

            if save_response.status_code == 200:
                st.success("Job saved successfully!")
                st.rerun()
            else:
                st.error("Save failed")
                st.write(save_response.text)


# My jobs (doesn't work right now)
elif page == "My Jobs":

    st.title("My Saved Jobs")

    if my_df.empty:
        st.info("No saved jobs yet.")
    else:
        st.metric("Saved Jobs", len(my_df))
        st.dataframe(my_df, use_container_width=True)



# Analytics
elif page == "Analytics":

    st.title("Analytics")

    if df.empty:
        st.info("No data available.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.histogram(df, x="keyword")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            top = df["company"].value_counts().reset_index()
            top.columns = ["company", "count"]
            fig2 = px.bar(top.head(10), x="company", y="count")
            st.plotly_chart(fig2, use_container_width=True)