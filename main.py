import certifi
import motor.motor_asyncio
from beanie import init_beanie
from beanie.odm.settings import document
from fastapi import FastAPI, Depends
from fastapi import Request, HTTPException, Header
from starlette.responses import JSONResponse

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://Naad:naad2002@cluster0.7redvzp.mongodb.net/",
    tlsCAfile=certifi.where(),
)
try:
    db = client.algotrading
except Exception as e:
    JSONResponse(
        {
            "message": "Database won't connect",
            "error_message": e,
        }
    )
    exit(1)


@app.on_event("startup")
async def start_database():
    await init_beanie(database=db, document_models=[])


@app.get("/")
async def home():
    metadata = {
        "name": "AlgoTradingCompetition",
        "description": "A platform for hosting IEEECS Algotrading Competition",
        "version": "1.0.0",
        "author": "Naad Dantale",
        "license": "MIT",
        "repository": "https://github.com/yourusername/AlgoTradingCompetition",
        "dependencies": {
            "fastapi": "0.70.0",
            "beanie": "0.16.3",
            # Add other dependencies and their versions here
        },
        "keywords": ["algorithmic trading", "competition", "API"],
        "contact": {
            "email": "your@email.com",
            "website": "https://www.yourwebsite.com",
        },
        "support": {
            "email": "support@yourwebsite.com",
            "documentation": "https://github.com/yourusername/AlgoTradingCompetition/wiki",
        },
    }
    return JSONResponse(content=metadata)
