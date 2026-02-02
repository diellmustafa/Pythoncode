import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv('BASE_URL')

api_key_input = st.text_input("Enter API Key", type="password")

def validate_api_key(api_key):
    headers = {"api-key": api_key}
    response = requests.get(f"{BASE_URL}/validate_key/", headers=headers)
    return response.status_code == 200

def get_authors():
    response = requests.get(f"{BASE_URL}/authors/")
    return response.json() if response.status_code == 200 else []

def add_author(api_key, name):
    headers = {"api-key": api_key}
    response = requests.post(f"{BASE_URL}/authors/", json={"name": name}, headers=headers)
    return response.status_code == 200

def update_author(api_key, author_id, name):
    headers = {"api-key": api_key}
    response = requests.put(f"{BASE_URL}/authors/{author_id}", json={"name": name}, headers=headers)
    return response.status_code == 200

def delete_author(api_key, author_id):
    headers = {"api-key": api_key}
    response = requests.delete(f"{BASE_URL}/authors/{author_id}", headers=headers)
    return response.status_code == 200

def get_books():
    response = requests.get(f"{BASE_URL}/books/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch books")
        return []

def add_book(api_key, book_data):
    headers = {"api-key": api_key}
    response = requests.post(f"{BASE_URL}/books/", json=book_data, headers=headers)
    if response.status_code == 200:
        st.success(f"Book '{book_data['title']}' added successfully!")
    else:
        st.error(f"Failed to add book: {response.json().get('detail', 'unknown error')}")

def update_book(api_key, book_id, book_data):
    headers = {"api-key": api_key}
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=book_data, headers=headers)
    if response.status_code == 200:
        st.success(f"Book '{book_data['title']}' updated successfully!")
    else:
        st.error(f"Failed to update book: {response.json().get('detail', 'unknown error')}")

def delete_book(api_key, book_id):
    headers = {"api-key": api_key}
    response = requests.delete(f"{BASE_URL}/books/{book_id}", headers=headers)
    if response.status_code == 200:
        st.success("Book deleted succesfully!")
    else:
        st.error(f"Failed to delete book: {response.json().get('detail', 'unknown error')}")
