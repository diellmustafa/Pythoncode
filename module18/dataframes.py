import pandas as pd
import streamlit as st

st.header("Displaying dataframes")

data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [22, 27, 32, 29, 25],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
})

st.dataframe(data)

# st.write(data)