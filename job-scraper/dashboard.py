import streamlit as st
import requests
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Job Scraper Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000"


# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# LOGIN / REGISTER PAGE
if not st.session_state.logged_in:
    st.title("🔐 Job Scraper Pro")
    st.caption("Login to access your personalized job dashboard")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_option = st.radio("Choose option", ["Login", "Register"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button(auth_option, use_container_width=True):
            endpoint = "/login" if auth_option == "Login" else "/register"

            try:
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

            except Exception as e:
                st.error("Failed to connect to API")
                st.write(str(e))

    st.stop()


# HEADER
header_col1, header_col2 = st.columns([6, 1])

with header_col1:
    st.title("💼 Job Scraper Pro")
    st.caption(f"Welcome back, {st.session_state.username}")

with header_col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.divider()


# FETCH DATA (USER-SPECIFIC)
jobs_response = requests.get(
    f"{API_URL}/jobs",
    params={"username": st.session_state.username}
)

if jobs_response.status_code == 200:
    jobs_data = jobs_response.json()
    df = pd.DataFrame(jobs_data) if jobs_data else pd.DataFrame()
else:
    st.error("Failed to fetch jobs")
    st.stop()

my_jobs_response = requests.get(
    f"{API_URL}/my-jobs/{st.session_state.username}"
)

if my_jobs_response.status_code == 200:
    my_jobs = my_jobs_response.json()
    my_df = pd.DataFrame(my_jobs) if my_jobs else pd.DataFrame()
else:
    my_df = pd.DataFrame()


# TOP TABS NAVIGATION
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Dashboard", "🔍 Job Explorer", "⭐ My Jobs", "📈 Analytics"]
)


# DASHBOARD TAB
with tab1:
    st.subheader("📊 Market Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Jobs", len(df))
    col2.metric("Saved Jobs", len(my_df))
    col3.metric("Companies", df["company"].nunique() if not df.empty else 0)
    col4.metric("Keywords", df["keyword"].nunique() if not df.empty else 0)

    st.divider()

    st.markdown("### 🔄 Scrape New Jobs")

    scrape_col1, scrape_col2 = st.columns([3, 1])

    with scrape_col1:
        keyword = st.text_input(
            "Enter job keyword",
            placeholder="python, backend, data analyst..."
        )

    with scrape_col2:
        st.write("")
        if st.button("🚀 Scrape Jobs", use_container_width=True):
            if keyword:
                with st.spinner("Scraping jobs..."):
                    response = requests.post(
                        f"{API_URL}/scrape/{keyword}",
                        params={"username": st.session_state.username}
                    )

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Scraped {data.get('scraped_jobs', 0)} jobs!")
                    st.rerun()
                else:
                    st.error("Scraping failed")
                    st.write(response.text)


# JOB EXPLORER TAB
with tab2:
    st.subheader("🔍 Explore Job Listings")

    if df.empty:
        st.info("No jobs available. Scrape jobs first.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            keyword_filter = st.selectbox(
                "Filter by Keyword",
                ["All"] + sorted(df["keyword"].dropna().unique().tolist())
            )

        with col2:
            company_filter = st.selectbox(
                "Filter by Company",
                ["All"] + sorted(df["company"].dropna().unique().tolist())
            )

        filtered_df = df.copy()

        if keyword_filter != "All":
            filtered_df = filtered_df[filtered_df["keyword"] == keyword_filter]

        if company_filter != "All":
            filtered_df = filtered_df[filtered_df["company"] == company_filter]

        st.dataframe(filtered_df, use_container_width=True, height=500)

        if not filtered_df.empty:
            st.markdown("### ⭐ Save a Job")

            job_options = {
                f"{row['title']} — {row['company']}": row["id"]
                for _, row in filtered_df.iterrows()
            }

            selected_job = st.selectbox(
                "Select a job to save",
                options=list(job_options.keys())
            )

            if st.button("💾 Save to My Jobs", use_container_width=True):
                job_id = job_options[selected_job]

                with st.spinner("Saving job..."):
                    save_response = requests.post(
                        f"{API_URL}/save-job",
                        json={
                            "username": st.session_state.username,
                            "job_id": job_id
                        }
                    )

                if save_response.status_code == 200:
                    st.success("Job saved successfully ⭐")
                else:
                    st.error("Save failed")
                    st.write(save_response.text)


# MY JOBS TAB
with tab3:
    st.subheader("⭐ My Saved Jobs")

    if my_df.empty:
        st.info("You haven't saved any jobs yet.")
    else:
        st.metric("Total Saved Jobs", len(my_df))
        st.dataframe(my_df, use_container_width=True, height=500)


# ANALYTICS TAB
with tab4:
    st.subheader("📈 Job Market Analytics")

    if df.empty:
        st.info("No data available yet.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Jobs by Keyword")
            fig1 = px.histogram(df, x="keyword")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown("#### Top Hiring Companies")
            top_companies = df["company"].value_counts().head(10)
            fig2 = px.bar(
                x=top_companies.index,
                y=top_companies.values,
                labels={"x": "Company", "y": "Job Count"}
            )
            st.plotly_chart(fig2, use_container_width=True)