import certifi
import motor.motor_asyncio
from beanie import init_beanie
from beanie.odm.settings import document
from fastapi import FastAPI, Depends
from fastapi import Request, HTTPException, Header
from pprint import pprint
from utils.authorize_key import fetch_api_key_roles

app = FastAPI()
kill_switch_enabled = False

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://Naad:naad2002@cluster0.7redvzp.mongodb.net/",
    tlsCAfile=certifi.where(),
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

keys_collection = db.keys


@app.on_event("startup")
async def start_database():
    await init_beanie(database=db, document_models=[])


@app.middleware("http")
async def middleware(request: Request, call_next, api_key: str = Header(None)):
    if request.url.path == "/toggle-kill-switch":
        response = await call_next(request)
        return response

    api_key_roles = await fetch_api_key_roles(keys_collection)

    # Check API key
    if api_key not in api_key_roles:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_role = api_key_roles[api_key]

    if kill_switch_enabled and user_role != "admin":
        raise HTTPException(
            status_code=503,
            detail="API disabled, Judging Round over",
        )

    response = await call_next(request)
    return response


@app.post("/toggle-kill-switch")
async def toggle_kill_switch(
    api_key: str = Header(None, description="API Key"),
):
    user_role = await fetch_api_key_roles(api_key)

    if user_role != "admin":
        raise HTTPException(
            status_code=403, detail="Forbidden. Only admins can toggle the kill switch."
        )

    global kill_switch_enabled
    kill_switch_enabled = not kill_switch_enabled
    return {
        "status": "Kill switch is now "
        + ("enabled" if kill_switch_enabled else "disabled")
    }


@app.get("/")
async def hello():
    return {"message": "hello brdr"}
