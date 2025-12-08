from http.client import HTTPException
from typing import List
from fastapi import FastAPI
import models
from models import Movie, MovieCreate
import database

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movies CRUD API"}

@app.post("/movies/", response_model=Movie)
def create_movie(movie: MovieCreate):
    #Creates a new movie in the database.
    movie_id = database.create_movie(movie)
    return models.Movie(id=movie_id, **movie.dict())

@app.get("/movies/", response_model=List[Movie])
def read_movies():
    #Reatrives all movies from the database
    return database.read_movies()

@app.get("/movies/{movie_id}", response_model=Movie)
def read_movie(movie_id: int):
    #Retreives a single movie
    movie = database.read_movie
    if movie in None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

