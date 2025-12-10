from pydantic import BaseModel
from typing import Optional

class RecipeBase(BaseModel):
    name: str
    description: Optional[str]
    ingredients: str
    instructions: str
    cuisine: str
    difficulty: str
    category_id: Optional[int]

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
