from fastapi import APIRouter, Body, HTTPException

from models.user import User, UserLogin
from models.trade import Account
from utils.auth.auth_handler import signJWT
from utils.create_secret import create_secret

router = APIRouter()


@router.post("/signup")
async def create_user(user: User = Body(...)):
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists."
        )

    # Create the User
    new_user = await user.create()

    # Create the Account
    account = Account(
        email=new_user.email,
        balance=2000,
        holdings={},
        trade_history=[],
        profit_loss=0.0,
    )
    existing_account = await Account.find_one(Account.email == account.email)
    if existing_account:
        raise HTTPException(status_code=400, detail="Account already exists")

    await account.create()

    secret = create_secret()
    return signJWT(user.email, role="participant", secret=secret)


@router.post("/login")
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

    secret = create_secret()
    if existing_user:
        return signJWT(email=str(user.email), role="participant", secret=secret)

    else:
        raise HTTPException(status_code=404, detail="User Not Found")
