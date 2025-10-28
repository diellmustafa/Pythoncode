import streamlit as st

tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.header("Content for tab1")
    st.write("This is the content for tab1")

with tab2:
    st.header("Content for tab2")
    st.write("This is the content for tab2")

with tab3:
    st.header("Content for tab3")
    st.write("This is the content for tab3")