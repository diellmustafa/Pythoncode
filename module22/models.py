from pydantic import BaseModel, ValidationInfo, field_validator

class User(BaseModel):
    id: int
    name: str
    age: int

    @field_validator('age')
    def age_must_be_positive(cls, v, info: ValidationInfo):
        if v <= 0:
            raise ValueError('Age must be positive')
        return v

try:
    user = User(id= 1, name = 'Alice', age = -1)
except ValueError as e:
    print(e)

#Nested Models

class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    id: int
    name: str
    address: Address