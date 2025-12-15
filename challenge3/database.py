import sqlite3
from challenge3.models.category import CategoryCreate, CategoryResponse, Category
from challenge3.models.recipe import RecipeCreate

DB_NAME = "recipes.db"


def create_connection():
    connection = sqlite3.connect("recipes.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_category_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()

create_category_table()

def get_categories():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()
    connection.close()
    categories = [Category(id=row[0], name=row[1]) for row in rows]
    return categories

def create_category(category: CategoryCreate) -> int:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (category.name))
    connection.commit()
    category_id = cursor.lastrowid
    connection.close()
    return category_id

def update_category(category_id: int, category: CategoryCreate) -> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE categories SET name=? WHERE id=?", (category.name, category_id))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0

def delete_category(category_id: int) -> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0

def create_recipe_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recipies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            category INTEGER AUTOINCREMENT
        )
        """
    )
    connection.commit()
    connection.close()

create_recipe_table()