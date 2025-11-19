from pydantic import BaseModel, conint, constr
from typing import Optional

# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#     email: str

# #validation

# user = User(id= 1, name = 'John Doe', age = 30, email = 'JohnDoe@example.com')

#default values and optional fields
class User(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    email: Optional[str] = None

user1 = User(id= 1, name = 'John Doe', age = 30, email = 'JohnDoe@example.com')
print(user1)

user2 = User(id= 2, name = 'Jane Doe', age = None, email = 'JaneDoe@example.com')
print(user2)

user3 = User(id= 3, name = 'Charlie', age = 30)
print(user3)

user4 =  User(id= 4, name = 'McGinn')
print(user4)

#field constraints
class another_user(BaseModel):
    id: conint(gt=0)
    name: constr(min_length=2, max_length=50)

valid_user = another_user(id= 1, name= 'Alice',)
print(valid_user)

# invalid_user = another_user(id=0, name= 'Alice')
# print(invalid_user)