from fastapi import FastAPI, HTTPException
from typing import List
import challenge3.database as database
import challenge3.models.category as models
from challenge3.models.category import CategoryCreate, Category, CategoryResponse


app = FastAPI()

@app.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate):
    category_id = database.create_category(category)
    return models.Category(id=category_id, **category.dict())

@app.get("/categories/", response_model=List[Category])
def get_categories():
    return database.get_categories()

@app.put("/category/{category_id}", response_model=Category)
def update_movie(category_id: int, category:models.CategoryCreate):
    updated = database.update_category(category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return models.Category(id=category_id, **category.dict())

@app.delete("/categories/{category_id}", response_model=Category)
def delete_category(category_id: int):
    deleted = database.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return{"message": "Movie deleted successfully"}