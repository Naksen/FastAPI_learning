import fastapi_users
from pydantic import BaseModel, Field
from fastapi import Depends, FastAPI
import sys

# setting path
sys.path.append('../')

from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from auth.database import User
from auth.auth import auth_backend

fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(
    title="Trading App"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def protected_route():
    return f"Hello, anonym"