from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import List
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import datetime
import json
from pathlib import Path

from model import UserCreate, User, Token

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/css", StaticFiles(directory="css"), name="css")

# Serve the HTML files from the "vues" directory
@app.get("/register")
def serve_register():
    return FileResponse("vues/register.html")

@app.get("/login")
def serve_login():
    return FileResponse("vues/login.html")

@app.get("/task")
def serve_dashboard():
    return FileResponse("vues/task.html")


# Token Utility
SECRET_KEY = "myjwtsecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

DATABASE_PATH = Path("db.json")





# Helper Functions to handle database I/O
def read_db():
    if DATABASE_PATH.exists():
        with open(DATABASE_PATH, "r") as f:
            return json.load(f)
    return []

def write_db(data):
    with open(DATABASE_PATH, "w") as f:
        json.dump(data, f, indent=4)


# Helper Functions for Password and Token Handling
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Routes
@app.post("/register", response_model=User)
def register_user(user: UserCreate):
    db = read_db()
    
    # Check if the email is already registered
    for db_user in db:
        if db_user['email'] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password and create a new user
    hashed_password = hash_password(user.password)
    new_user = {
        "id": len(db) + 1,
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_password,
        "todos": []
    }
    
    # Add the new user to the database and save it
    db.append(new_user)
    write_db(db)
    
    return new_user



@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = read_db()
    
    # Find the user by email
    user = None
    for db_user in db:
        if db_user['email'] == form_data.username:
            user = db_user
            break

    # Verify password
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Create a token
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/todos",status_code=status.HTTP_201_CREATED)
def add_todo(title: str, description: str, token: str = Depends(oauth2_scheme)):
    db = read_db()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    print(email)
    user = None
    for db_user in db:
        if db_user["email"] == email:
            user = db_user
            break

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Create a new todo and add it to the user's todos
    todo = {
        "id": len(user["todos"]) + 1,
        "title": title,
        "description": description,
        "start": datetime.datetime.now().strftime("%Y-%m-%d"),
        "end": (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
        "priority": "high"
    }
    user["todos"].append(todo)

    # Save the updated database
    write_db(db)

    return {"msg": "Todo added", "todo": todo}




if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
