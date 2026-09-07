from fileinput import filename
import sqlite3
from turtle import title

from fastapi import Header, Depends, FastAPI , status , HTTPException , Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time as Time
from passlib.context import CryptContext
app = FastAPI()



# users route
@app.get("/users/{user_id}")
def get_user(user_id:int):
    return {"user_id": user_id}




# QUERRY PARAMETERS::::::::::
# 1.optional parameters:
@app.get("/users")
def get_users(name: str=None):
    return{"Name":name}

# 2.default parameters:
@app.get("/products")
def get_product(limit: int=10):
    return{"limit":limit}

# multiple querry parameters: 
@app.get("/items")
def get_users(name:str=None , price :int=0 ):
    return{"Name":name , "Price":price}





# REQUEST BODY:::::::::::::::::::::::::::::
1.post request:
@app.post("/create_user")
def users(name:str , age:int):
    return{"Name":name , "age":age}
# as a dict also we can see for json output
@app.post("/create_user")
def users(user:dict):
    return{
        "message":"User Created",
        "data":user
    }


# pydantic model:
class User(BaseModel):
    name:str
    age:int
    email:str
@app.post("/create_user")
def users(user:User):
    return{
        "message":"User Created",
        "data":user
    }
    
# loops in pydantic:
class Address(BaseModel):
    city:str
    pin:int
    
class User(BaseModel):
    name:str
    age:int
    address:Address    
    
@app.post("/create_users")
def create_user(user:User):
    return user  




# CRUD OPERATIONS:::::::::::::

todos=[] 
class Todo(BaseModel):
    id:int
    title:str
    completed:bool
    
@app.post("/todos") #create
def create_todo(todo:Todo):
    todos.append(todo)
    return {"message":"TODO added" , "data":todo}   

@app.get("/todos") #retrive
def get_todos():
    return todos

@app.get("/todos/{todo_id}") #retrive based on id  ....url..../todos/id        ->> id like 1, 2 , 3, 4 etc
def get_todo(todo_id:int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return{"error":"Todo not found"}    
    

@app.put("/todos/{todo_id}")  #update
def update_todo(todo_id:int , updated_todo:Todo):
    for index , todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = update_todo
            return{
            "message":"Data updated" , 
            "data": update_todo
            }
    return {"error":"todo not found"}    



@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return{"message":"data deletd"}
    return{"error":"Todo not Found"}
    
    
    

# Path / Querry/ Body Combo

users =[]

class User(BaseModel):
    name:str
    age:int
    
@app.post("/users")
def create_user(user:User):
    users.append(user)
    return{
        "message":"user created",
        "data":user
    }    
    
@app.put("/users/{user_id}")
def updated_user(user_id:int, user:User,notify:bool=False):
    if user_id< len(users):
        users[user_id]=user
        
        return{
            "message":"user updated",
            "notify":notify,
            "data":user
        }
    return{
        "error":"user not found"
    }    
    
    
    
# RESPONSE MODEL:::::::::::::::
class User(BaseModel):
    name:str
    age:int
    password:str
    
class UserResponse(BaseModel):
    name:str
    age:int
    
@app.get("/users/{user_id}", response_model=UserResponse)    # here we are using response model to format the output and password will not be shown in output
def get_user() :
    return{
        "name":"John",
        "age":30    #output formatting will be done by response model and password will not be shown in output
    }





#   STATUS CODE::::::::::::::: AND  RESPONSE MODEL::::::::::::::: 
# 1. http status code:
@app.post("/create_user", status_code= status.HTTP_201_CREATED)   
def create_user():
    return{
        "message":"User Created"
    }

# 2. custom response kaise bhej sakte hai :
@app.get("/users")
def get_users():
    return{
        "status":"success",
        "name":"John",
        "age":30
    }    
    
#  BASIC Exception HANDELING:::::::::::::::: 

@app.get("/users/{user_id}")
def get_users(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return{
        "id":1,
        "name":"John",
        "age":30
    }


# custom exception handling:
class UserNotFoundException(Exception):
    def __init__(self, user_name: str):
        self.user_name = user_name

# global exception handeler for UserNotFoundException
@app.exception_handler(UserNotFoundException)
def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"User '{exc.user_name}' not found."},
    )
@app.get("/users/{user_name}") # dynamic route
def get_user(user_name: str):
    if user_name != "John":
        raise UserNotFoundException(user_name)
    return {
        "name": user_name
    }        





#  DEPENDENCY INJECTION:::::::::::::::
# def common_logic():
#     return {"message": "This is a common logic"}

# @app.get("/home")
# def home(data=Depends(common_logic)): #wrapping the common logic function with Depends() to inject the dependency into the home route
#     return data

# reusable  dependency injection:
# def get_current_user():
#     return {"user": "John"}
# @app.get("/profile")
# def profile(user=Depends(get_current_user)):
#     return user
# @app.get("/dashboard")
# def dashboard(user=Depends(get_current_user)):
#     return user

# Authentication dependency injection:
def get_current_user(token: str = Header(None)):
    if token != "valid_token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"user": "John"}

@app.get("/secured-data")
def secured_data(user=Depends(get_current_user)):
    return {"message": "This is secured data", "user": user}




# MIDDLEWARE:::::::::::::::
@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = Time.time() # Record the start time
    # Log the request details
    print(f"Request: {request.method} {request.url}")
    
    # Call the next middleware or route handler
    response = await call_next(request)  #await call_next(request) is used to pass the request to the next middleware or route handler in the chain. It allows the request to continue its journey through the middleware stack and eventually reach the appropriate route handler for processing.
    
    process_time = Time.time() - start_time
    # Log the processing time
    print(f"Processing Time: {process_time}")
    # Log the response details
    print(f"Response: {response.status_code}")
    
    return response






#  SQLite database integration with FastAPI:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import sqlite3
from fastapi import FastAPI, HTTPException
app = FastAPI()
conn = sqlite3.connect("mydatabase.db", check_same_thread=False)  # Create a connection to the SQLite database
cursor = conn.cursor()  # Create a cursor object to execute SQL queries
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')  # Create a table if it doesn't exist

conn.commit()  # Commit the changes to the database

@app.get("/home")
def home():
    return {"message": "Welcome to the FastAPI SQLite example!"}






# SQLALchemy integration with FastAPI:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends, HTTPException
app = FastAPI()

DATABASE_URL = "sqlite:///./mydatabase2.db"  # SQLite database URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Create a SQLAlchemy engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()  # Create a base class for SQLAlchemy models

class Todo(base):
    __tablename__ = "todos"  # Table name in the database
    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    title = Column(String, index=True)  # Title column
    completed = Column(Integer, default=0)  # Completed column (0 for False, 1 for True)
    
base.metadata.create_all(bind=engine)  # Create the table in the database    

def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session to be used in route handlers
    finally:
        db.close()  # Close the session after use
        

# create api to add a new todo to the database
@app.post("/todos")  # create api to add a new todo to the database
def create_todo(title: str, db: Session = Depends(get_db)):
    todo = Todo(title=title, completed=0)  # Create a new Todo object with the provided title
    db.add(todo)  # Add the Todo object to the database session
    db.commit()  # Commit the changes to the database
    db.refresh(todo)
    return {"message": "Todo added successfully", "data": {"id": todo.id, "title": todo.title, "completed": todo.completed}}  # Return a success message with the added Todo details


# read data based on id from database
@app.get("/todos/{todo_id}")  # create api to read data based on id from database
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()  # Query the database for a Todo with the specified id
    if not todo:  # If no Todo is found, raise an HTTPException with a 404 status code
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"id": todo.id, "title": todo.title, "completed": todo.completed}  # Return the details of the found Todo        

# read all data from database
@app.get("/todos")  # create api to read all data from database
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()  # Query the database for all Todo objects
    return [{"id": todo.id, "title": todo.title, "completed": todo.completed} for todo in todos]  # Return a list of all found Todos 







# UPDATE DATA IN DATABASE:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@app.put("/todos/{todo_id}")  # create api to update data in database 
def update_todo(todo_id: int, title: str, completed: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()  # Query the database for a Todo with the specified id
    if not todo:  # If no Todo is found, raise an HTTPException with a 404 status code
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = title  # Update the title of the found Todo
    todo.completed = completed  # Update the completed status of the found Todo
    db.commit()  # Commit the changes to the database
    db.refresh(todo)  # Refresh the Todo object with the updated values
    return {"message": "Todo updated successfully", "data": {"id": todo.id, "title": todo.title, "completed": todo.completed}}  # Return a success message with the updated Todo details





# DELETE DATA IN DATABASE:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@app.delete("/todos/{todo_id}")  # create api to delete data in database
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()  # Query the database for a Todo with the specified id
    if not todo:  # If no Todo is found, raise an HTTPException with a 404 status code
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)  # Delete the found Todo from the database
    db.commit()  # Commit the changes to the database
    return {"message": "Todo deleted successfully"}  # Return a success message






# ASYNC PROGRAMMING WITH FASTAPI:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# normal time handling function
# import time 
# def task():
#     time.sleep(5)  # Simulate a time-consuming task by sleeping for 5 seconds
#     return "Task completed"  # Return a message indicating that the task is completed

# async time handling function
# import asyncio

# async def async_task():
#     await asyncio.sleep(5)  # Simulate a time-consuming task by sleeping for 5 seconds
#     return "Task completed"  # Return a message indicating that the task is completed


# async method from fastapi

import time
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/async-task")
async def run_async_task():
    await asyncio.sleep(5)  # Simulate a time-consuming task by sleeping for 5 seconds
    return {"message": "Async task completed"}  # Return a message indicating that the async








# AUTHENTICATION AND AUTHORIZATION WITH FASTAPI:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# jwt authentication with fastapi
from fastapi import FastAPI, Depends, HTTPException, status,Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


app = FastAPI()

SECRET_KEY = "mysecret"  # create a secret key for JWT token generation
ALGORITHM = "HS256" # algorithm used for JWT token generation
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # token expiration time in minutes


# create token for user authentication and authorization
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()  # Create a copy of the data to encode
    if expires_delta:  # If an expiration time is provided
        expire = datetime.utcnow() + expires_delta  # Calculate the expiration time
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default expiration time is 15 minutes
    to_encode.update({"exp": expire})  # Add the expiration time to the data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the data into a JWT token
    return encoded_jwt  # Return the encoded JWT token

# token generation endpoint
@app.post("/login")
async def login_for_access_token(username:str, password:str):
    if username != "admin" or password != "password":  # Check if the provided username and password are valid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # Raise an HTTPException with a 401 status code for invalid credentials
            detail="Incorrect username or password",  # Provide a detail message for the exception
            headers={"WWW-Authenticate": "Bearer"},  # Set the WWW-Authenticate header to indicate that Bearer authentication is required
        )
    token = create_access_token(data={"sub": username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))  # Create an access token for the authenticated user
    return {"access_token": token, "token_type": "bearer"}  # Return the access token and token type in the response

# token verification endpoint
def token_verify(token:str=Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the JWT token using the secret key and algorithm
        username: str = payload.get("sub")  # Extract the username from the decoded payload
        if username is None:  # If the username is not found in the payload
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,  # Raise an HTTPException with a 401 status code for invalid token
                detail="Invalid token",  # Provide a detail message for the exception
                headers={"WWW-Authenticate": "Bearer"},  # Set the WWW-Authenticate header to indicate that Bearer authentication is required
            )
        return username  # Return the extracted username
    except JWTError:  # If there is an error decoding the JWT token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # Raise an HTTPException with a 401 status code for invalid token
            detail="Invalid token",  # Provide a detail message for the exception
            headers={"WWW-Authenticate": "Bearer"},  # Set the WWW-Authenticate header to indicate that Bearer authentication is required
        )
        
        

# protected route that requires token verification
@app.get("/protected")
async def read_protected_data(current_user: str = Depends(token_verify)):
    
    return {"message": "This is a protected route", "user": current_user}






# OAUTH + JWT:::


#from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import hashlib  # <--- SABSE IMPORTANT

app = FastAPI()

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 1. Context to banao
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. 🔥 SHIELD FUNCTION 1: Hash karne ke liye (Sirf yahi se hash hoga)
def hash_password(password: str) -> str:
    # Pehle SHA256 (fixed 64 chars, 72 bytes se chhota), phir bcrypt
    sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(sha256_hash)

# 3. 🔥 SHIELD FUNCTION 2: Verify karne ke liye (Sirf yahi se verify hoga)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Pehle plain password ko bhi SHA256 mein convert karo, phir compare karo
    sha256_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 4. Database mein hash DALTE WAQT 'hash_password' function use karo (direct nahi)
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": hash_password("adminpassword")  # <--- Yahan function call karo
    }
}

# 5. Token create function
def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 6. Login Endpoint (Verify karne ke liye 'verify_password' function use karo)
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):  # <--- Yahan function call
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# 7. Token Verify
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 8. Protected Route
@app.get("/protected")
def read_protected_data(current_user: str = Depends(verify_token)):
    return {"message": "This is a protected route", "user": current_user}







# FILE UPLOAD + sERVER STATIC::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
from fastapi import FastAPI, UploadFile , File, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import shutil
app = FastAPI()

# step1: Ensures uploads folder exist

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
#STEP2 : Static file set-up

app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files") 


# step 3 create a upload file API
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": f"File saved at {file_location}"}

# step 4: get file url api
@app.get("/files/{file_name}")
def get_file(file_name:str):
    file_location = os.path.join(UPLOAD_DIR, file_name)
    
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    return{
        "file_url":f"http://127.0.0.1:8000/files/{file_name}"
    }

@app.get("/")
def home():
    return{
        "message":"file uploaded api running"
    }








# CORS (Cross-Origin Resource Sharing) IN FASTAPI:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
#   allowed origins for CORS(frontend url)
origins = [
    "http://localhost:3000",  # React frontend
]

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from the specified origins
    allow_credentials=True,  # Allow cookies and credentials to be included in requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers in requests
)

@app.get("/")
def home():
    return {"message": "CORS enabled FastAPI application is running!"}






ENVIRONMENT VARIABLES IN FASTAPI:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::






# API Testing with FastAPI: Pytest::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b} 







THIRD PARTY API INTEGRATION WITH FASTAPI:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


using basic python requests library to fetch data from third-party API
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts")
data = response.json()
if response.status_code == 200:
    data = response.json()
    print(data)



# using fastapi to fetch data from third-party API
from fastapi import FastAPI
import requests

app=FastAPI()

# get all data from third-party API
@app.get("/posts")
def get_posts():
    url="https://jsonplaceholder.typicode.com/posts"
    response=requests.get(url)
    
    return response.json()
    

# get single data from third-party API based on id
@app.get("/posts/{post_id}")
def get_post(post_id:int):
    url=f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response=requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Error fetching data from third-party API")
    return response.json()
    
    
    





# WEB CRAWLER  AND PAGINATION  AND CACHING WITH FASTAPI:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
import time


app = FastAPI()


# cache storage
cache_data = {}
last_cache_time = {}
CACHE_EXPIRATION = 60  # cache expiration time in seconds


@app.get("/scrape")
def scrape_website(
    url: str = "https://news.ycombinator.com/news",
    page: int = 1,
    limit: int = 5
):
    global cache_data, last_cache_time

    # Validate page and limit
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be greater than or equal to 1"
        )

    if limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Limit must be greater than or equal to 1"
        )

    start = time.time()

    # Create unique cache key for URL + page
    cache_key = f"{url}?p={page}"

    current_time = time.time()

    # Check if fresh data exists in cache
    if (
        cache_key in cache_data
        and cache_key in last_cache_time
        and current_time - last_cache_time[cache_key] < CACHE_EXPIRATION
    ):
        print("using fresh data from cache")

        data = cache_data[cache_key]

    else:
        print("fetching fresh data from website")

        # Pagination
        page_url = f"{url}?p={page}"

        try:
            response = requests.get(
                page_url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            response.raise_for_status()

        except requests.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch website: {str(e)}"
            )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Extract news titles
        data = [
            item.get_text(strip=True)
            for item in soup.select("span.titleline > a")
        ]

        # Store data in cache
        cache_data[cache_key] = data
        last_cache_time[cache_key] = time.time()

    end = time.time()

    time_taken = round(end - start, 4)

    print("time taken:", time_taken)

    return {
        "page": page,
        "limit": limit,
        "time_taken": time_taken,
        "data": data[:limit]
    }









# RATE LIMITING:::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse


app= FastAPI()


# limiter setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# error handel
@app.exception_handler(RateLimitExceeded)
def rate_limit_handeler(request:Request, exc:RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail":"too many Requests"
        }
    )
    
    # rate limiter
@app.get("/data")
@limiter.limit("5/minute")
def get_data(request:Request):
    return{
            "message":"Success"
        }