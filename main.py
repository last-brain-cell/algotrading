from pprint import pprint
import certifi
import motor.motor_asyncio
import uvicorn
from beanie import init_beanie
from fastapi import FastAPI, Depends
from fastapi import Request, HTTPException, Header
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from models.trade import Account
from models.user import User
import Routes.login
import Routes.trade
import Routes.stocks
import Routes.admin
from utils.auth.auth_bearer import JWTBearerAdmin

app = FastAPI()
kill_switch_enabled = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# client = motor.motor_asyncio.AsyncIOMotorClient(
#     "mongodb+srv://Naad:naad2002@cluster0.7redvzp.mongodb.net/",
#     tlsCAfile=certifi.where(),
# )
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017/",
)

try:
    db = client.algotrading
except Exception as e:
    pprint(
        {
            "message": "Database won't connect",
            "error_message": e,
        }
    )
    exit(1)


@app.on_event("startup")
async def startup_database():
    await init_beanie(database=db, document_models=[User, Account])


@app.middleware("http")
async def middleware(request: Request, call_next):
    if request.url.path == "/toggle-kill-switch":
        response = await call_next(request)
        return response

    if kill_switch_enabled:
        raise HTTPException(
            status_code=503,
            detail="API disabled, Judging Round over",
        )

    response = await call_next(request)
    return response


@app.post(
    "/toggle-kill-switch", dependencies=[Depends(JWTBearerAdmin())], tags=["Home"]
)
async def toggle_kill_switch():
    global kill_switch_enabled
    kill_switch_enabled = not kill_switch_enabled
    return {
        "status": "Kill switch is now "
        + ("enabled" if kill_switch_enabled else "disabled")
    }


@app.get("/", tags=["Home"])
async def metadata():
    current_datetime = datetime.now()

    metadata = {
        "metadata": {
            "name": "AlgoTradingCompetition",
            "description": "Backend for the platform for hosting MUJ IEEE Computer Society Algotrading Competition",
            "version": "1",
            "author": "Naad Dantale",
            "repository": "https://github.com/last-brain-cell/algotrading",
            "dependencies": {
                "fastapi": "0.104.0",
                "beanie": "1.23.0",
                "pydantic": "2.4.2",
                "pymongo": "4.5.0",
                "uvicorn": "0.23.2",
                "pyJWT": "2.8.0",
                "python-decouple": "3.8",
                "decouple": "0.0.7",
                "certifi": "2023.7.22",
                "motor": "3.3.1",
                "email-validator": "2.1.0",
                "cryptography": " ",
            },
            "keywords": ["algorithmic trading", "competition", "API"],
            "contact": {
                "email": "naadkd@gmail.com",
                "mobile": "+91 7722087410",
            },
        },
        "last_ran": current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return JSONResponse(content=metadata)


app.include_router(Routes.login.router, tags=["User"], prefix="/user")
app.include_router(Routes.trade.router, tags=["Trade"], prefix="/trade")
app.include_router(Routes.stocks.router, tags=["Stock"], prefix="/stock")
app.include_router(Routes.admin.router, tags=["Admin"], prefix="/admin")

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000, reload=True)
