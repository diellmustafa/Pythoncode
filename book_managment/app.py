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
        st.success("Book deleted successfully!")
    else:
        st.error(f"Failed to delete book: {response.json().get('detail', 'unknown error')}")


def dashboard_author(api_key):
    st.title('author Management Dashboard')
    st.subheader('existing authors')
    authors = get_authors()
    df_authors = pd.DataFrame(authors)
    st.dataframe(df_authors, use_container_width=True)

    st.subheader('add new authors')
    new_author_name = st.text_input('Author Name')

    if st.button('Add Author'):
        if new_author_name.strip():
            add_author(api_key, new_author_name)
        else:
            st.error("Author name cannot be empty")

    action = st.radio('Select Action', options=['Update Author', 'Delete Author'])

    if action == 'Update Author':
        selected_author = st.selectbox('Select author to Update', options = [author['name'] for author in authors])
        new_name = st.text_input('New Author Name', value=selected_author)

        if st.button('Update Author'):
            author_id = next((author['id'] for author in authors if author ['name']==selected_author), None)
            update_author(api_key, author_id, new_name)

    if action == 'Delete Author':
        author_to_delete = st.selectbox('Select Author to Delete', options=[author['name'] for author in authors])
        if st.button('Delete Author'):
            author_id = next((author['id'] for author in authors if author['name']==author_to_delete), None)
            delete_author(api_key, author_id)


st.subheader('Existing Books')
books = get_books()
author = get_authors()

author_id_to_name = {author['id']: author['name'] for author in author}

for book in books:
    book['author']
    book['author_name'] = author_id_to_name.get(book['author'], 'Unknown Author')
    book['genres'] = ', '.join(book['genres'])
    del book ['author_id']

df_books = pd.DataFrame(books)
st.dataframe(df_books, use_container_width=True)

st.subheader('Add New Book')
new_book_title = st.text_input('Book Title')
selected_author = st.text_input('Selected Author', options=[author['name'] for author in author], key = "select_author_add")
new_book_average = st.number_input('Average Rating', min_value = 0.0, max_value = 5.0, step = 0.1)
new_book_genres = st.text_input('Genres (comma separated)')
new_book_year = st.number_input('Publication Year', min_value=1440,max_value=datetime.now().year,step=1)

if st.button('Add Book'):
    if new_book_title.strip() and new_book_genres.strip():
        genres_list = [g.strip() for g in new_book_genres.split(',') if g.strip()]
        selected_author_id = next ((author['id'] for author in author if author['name']==selected_author), None)


        book_data = {
            "title": new_book_title,
            "author_id": selected_author_id,
            "book_Link": "",
            "average_rating": new_book_average,
            "genres": genres_list,
            "published_year": new_book_year
        }
        add_book(api_key, book_data)
    else:
        st.error("Book title and genres cannot be empty")

action = st.radio('Select Action', options=['Update Book', 'Delete Book'], key='book_action')

if action == 'Update Book':
    selected_book = st.selectbox('Select book to update', options=[book['title'] for book in books], key='select_book_update')

    if selected_book:
        book = next((book for book in books if book['title']==selected_book), None)
        new_book_title = st.text_input(' Book Title', value=book['title'])
        selected_author_name = st.selectbox('Select Author', options=[author['name'] for author in author], index=[author['name'] for author in author].index(book['author_name']))
        new_book_average_rating = st.number_input('Average Rating', min_value = 0.0, max_value = 5.0, step = 0.1, value=book['average_rating'])
        new_book_genres = st.text_input('Genres (comma separated)', value=book['genres'])
        new_book_year = st.number_input('Publication Year', min_value=1440, max_value=datetime.now().year,step=1,value=book['publication_year'])
        book_id = book['id']

        if st.button("Update Book"):
            genres_list = [g.strip() for g in new_book_genres.split(',') if g.strip()]
            book_data = {
                "title": new_book_title,
                "author_id": next((author['id'] for author in authors if author['name'] == selected_author_name), None),
                "rating": book.get('book_link', ""),
                "genres": genres_list,
                "average_rating": new_book_average,
                "published_year": new_book_year
            }
            update_book(api_key, book_id, book_data)

elif action == "Delete Book":
    book_to_delete = st.selectbox("Select Book to Delete", options=[book['title'] for book in books], key="select_book_delete")

    if st.button("Delete Book"):
        book_id = next((book['id'] for book in books if book['title'] == book_to_delete), None)
        delete_book(api_key, book_id)


#Creating Visualization
def visualization_dashboard():
    st.title("Visualization Dashboard")

    book = get_books()
    authors = get_authors()

    df_books = pd.DataFrame(books)

    if 'author_id' in df_books.columns:
        author_id_to_name = {author['id']: author['name'] for author in authors}
        df_books['author'] = df_books['author_id'].map(author_id_to_name)
        df_books.drop('author_id', axis=1, inPlace=True)

    st.sidebar.title("Filters")

    selected_author = st.sidebar.selectbox("Select Author", options=["All"] + list(author_id_to_name.values()))

    min_year = int(df_books['published_year'].min())
    max_year = int(df_books['published_year'].max())
    selected_year = st.sidebar.slider("Select Published Year", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    selected_rating = st.sidebar.slider("Select Average Rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.1)

    filters_applied = selected_author !="All" or selected_year !=(min_year, max_year) or selected_rating != (0.0, 5.0)

    if st.sidebar.button("Apply Filters") or not filters_applied:
        filters_books = df_books.copy()

        if filters_applied:
            if selected_author != "All":
                filters_books = filters_books[filters_books['author'] == selected_author]

                filters_books = filters_books[(filters_books['published_year'] >= selected_year[0]) & (
                filters_books['published_year'] <= [1])]

                filters_books = filters_books[(filters_books['average_rating'] >= selected_rating[0]) & (
                filters_books['average_rating'] <= [1])]


        if not filters_books.empty:
            st.subheader(f"Books by Year")
            books_by_year = filters_books.groupby('published_year').size().reset_index(name='Count')
            fig_years = px.bar(
                books_by_year,
                x = 'published_year',
                y = 'Count',
                title=f'Number of Books by Year',
                labels={"published_year": "Published Year", "Count": "Number of Books"},
                text='Count'
            )
            fig_years.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig_years.update_layout(
                informtext_minsize = 8,
                uniformtext_mode = 'hide',
                xaxis = dict(
                    tickmode='linear',
                    tick0=min_year,
                    dtick=5,
                    tickangle=-45,
                    tickfront=dict(size=10)
                ),
                yaxis = dict(title='Number of Books', range=[0, books_by_year['Count'].max() + 1]),
                title_x = -0.5
            )
            st.plotly_chart(fig_years, use_container_width=True)

            st.subheader(f"Books by Average Rating")
            books_by_rating = filters_books.groupby('average_rating').size().rest_index(name='Count')
            fig_ratings = px.bar(
                books_by_rating,
                x = 'average_rating',
                y = 'Count',
                title = "Number of Books by Average Rating",
                labels = {"average_rating": "Average Rating", "Count": "Number of Books"},
                text='Count'
            )
            fig_ratings.update_traces()
            fig_ratings.update_layout(
                informtext_minsize=8,
                uniformtext_mode='hide',
                yaxis=dict(title='Number of Books', range=[0, books_by_rating['Count'].max() + 1]),
                title_x=0.5
            )
            st.plotly_chart(fig_ratings, use_container_width=True)
        else:
            st.warning("No book data available for the selected filters")
    else:
        st.warning("No book data available for visualization")

st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose a dashboard", ["Authors Dashboard", "Visualization"])
if option == "Visualization":
    visualization_dashboard()
if api_key_input and validate_api_key(api_key_input):
    if option == "Authors Dashboard":
        dashboard_author(api_key_input)
else:
    st.error("Invalid API Key or API Key is missing")