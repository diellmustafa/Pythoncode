import sqlite3
from models import MovieCreate, Movie

def create_connection():
    #Creates a connection to the sqlite database
    connection = sqlite3.connect("movies.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    #Creates the movies table in the database if it doesn't exist
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()

create_table()

def create_movie(movie: MovieCreate) -> int:
    #Adds a new movie to the database
    #args: movie (MovieCreate): A pydantic model containing the title and director of the movie created
    #Returns: Int- the  ID of the newley created movie in the database.

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO movies (title, director) VALUES (?, ?)", (movie.title, movie.director))
    connection.commit()
    movie_id = cursor.lastrowid
    connection.close()
    return movie_id

def read_movies():
    #Reatrieves all movies from the database
    connection = create_connection()
    cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    connection.close()
    movies = [Movie(id=row[0], title=row[1], director=row[2]) for row in rows]
    return movies

def read_movie(movie_id: int):
    #Retrieves a single movie from database by its ID.
    #Return: Movie: A movie model respreting the retrieved movie, return none if the movie is not found

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return Movie(id=row["id"], title=row["title"], director=row["director"])

def update_movie(movie_id: int, movie: MovieCreate) -> bool:
    #Updated an existing movie in the database
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE movies SET title=?, director=? WHERE id=?", (movie.title, movie.director, movie_id))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0

def delete_movie(movie_id: int) -> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELTE FROM movies WHERE id = ?", (movie_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0