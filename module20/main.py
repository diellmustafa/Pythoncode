from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def root():
    return{"message": "Hello World"}

#uvicorn main:app --reload

@app.get("/greet/")
def read_root(name: str):
    return{"message": f"Hello, {name}!"}