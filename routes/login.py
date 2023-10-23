from typing import List, Dict
from fastapi import APIRouter, Body, Query, HTTPException
from models.user import User, UserSignup, UserLogin
from models.trade import Account
from utils.auth_handler import signJWT
from utils.create_secret import create_secret

router = APIRouter()


@router.post("/signup", tags=["user"])
async def create_user(user: UserSignup = Body(...)):
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists."
        )

    new_user = await User(**user.dict()).create()

    account = Account(participant_id=new_user.email, balance=0, holdings={})
    await account.create()

    token = signJWT(new_user.email, role="participant", secret=create_secret())
    return {"user": new_user, "team_name": new_user.team_name, "token": token}


@router.post("/login", tags=["user"])
async def user_login(user: UserLogin = Body(...)):
    existing_user = await User.find_one(
        User.email == user.email and User.password == user.password
    )
    if not existing_user:
        wrong_password = await User.find_one(User.password == user.password)
        wrong_email = await User.find_one(User.password == user.password)
        if wrong_password or wrong_email:
            raise HTTPException(
                status_code=401,
                detail="Login failed. Please check your email and password.",
            )

    if existing_user:
        token = signJWT(email=user.email, role="participant", secret=create_secret())
        return {
            "user": existing_user,
            "team_name": existing_user.team_name,
            "token": token,
        }
    else:
        raise HTTPException(status_code=404, detail="User Not Found")
