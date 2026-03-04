#NOTE: OLD CODE, IS NOT USED


# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
#
#
#
# API_URL = "http://127.0.0.1:8000"
#
# st.sidebar.title("Authentication")
#
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#
# # Login/Register UI
# if not st.session_state.logged_in:
#     st.subheader("Login or Register")
#
#     auth_option = st.radio("Choose option", ["Login", "Register"])
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#
#     if st.button(auth_option):
#         endpoint = "/login" if auth_option == "Login" else "/register"
#
#         try:
#             response = requests.post(
#                 f"{API_URL}{endpoint}",
#                 json={"username": username, "password": password}
#             )
#
#             # DEBUG: show raw response if something breaks
#             if response.status_code != 200:
#                 st.error(f"API Error: {response.status_code}")
#                 st.write(response.text)
#                 st.stop()
#
#             data = response.json()
#
#         except Exception as e:
#             st.error("Failed to connect to API")
#             st.write(str(e))
#             st.stop()
#
#         if "error" in data:
#             st.error(data["error"])
#         else:
#             st.success(data.get("message", "Success"))
#
#             if auth_option == "Login":
#                 st.session_state.logged_in = True
#                 st.session_state.username = username
#                 st.rerun()
#
#     st.stop()
#
# st.title("Job Listings Scraper & Analyzer")
#
# keyword = st.text_input("Enter job keyword: ", "python")
#
# if st.button("Scrape Jobs"):
#     response = requests.post(
#         f"{API_URL}/scrape/{keyword}",
#         params={"username": st.session_state.username}
#     )
#
#     if response.status_code == 200:
#         data = response.json()
#         scraped_count = data.get("scraped_jobs", 0)
#         st.success(f"Scraped {scraped_count} jobs!")
#     else:
#         st.error(f"Error: {response.status_code}")
#         st.write(response.text)
#
# # Fetch jobs
# response = requests.get(
#     f"{API_URL}/my-jobs",
#     params={"username": st.session_state.username}
# )
#
# if response.status_code == 200:
#     data = response.json()
#
#     if data:
#         df = pd.DataFrame(data)
#
#         st.subheader("Job Listings")
#         st.dataframe(df)
#
#         st.subheader("Jobs by Keyword")
#         fig1 = px.histogram(df, x="keyword")
#         st.plotly_chart(fig1)
#
#         st.subheader("Top Hiring Companies")
#         top_companies = df["company"].value_counts().reset_index()
#         top_companies.columns = ["company", "count"]
#
#         fig2 = px.bar(top_companies.head(10), x="company", y="count")
#         st.plotly_chart(fig2)
#     else:
#         st.info("No jobs in database yet. Run the scraper!")
#
