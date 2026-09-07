from fastapi import FastAPI

app = FastAPI()



# HOME ROUTE
@app.get("/")
def home():
    return {"message": "hello without venv"} 


# ABOUT ROUTE
@app.get("/about")
def about():
    return{"message": "ka raja ka haal ba"}


# USERS ROUTE
@app.get("/users")
def users():
    return{"message": "ka babuan ji , sb theek ba nu" , 
            "users":["mohit" , "rohit", "betichod hai"]
            }