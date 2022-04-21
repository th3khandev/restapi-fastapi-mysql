from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User

from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user_routes = APIRouter()

@user_routes.get("/users")
def get_users():
    return conn.execute(users.select()).fetchall()

@user_routes.post("/users")
def create_user(user: User):
    new_user = {
        "name": user.name,
        "email": user.email
    }
    new_user["password"] = f.encrypt(user.password.encode("utf-8")).decode("utf-8")
    print(new_user)
    result = conn.execute(users.insert(), new_user)
    print(result)
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()