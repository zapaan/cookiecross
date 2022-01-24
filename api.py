from typing import Optional
import uuid

from fastapi import FastAPI, Response, Cookie
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_data = {}
script_data = {
    "tracking": {
        "https://example.com/script.js",
        "https://example.com/script2.js",
        "https://example.com/script11.js",
    },
    "not_tracking": {
        "https://example.com/script3.js",
        "https://example.com/script4.js",
        "https://example.com/script5.js",
        "https://example.com/script11.js",
    }
}

class ConsentInput(BaseModel):
    tracking: bool = False
    not_tracking: bool = False


def handle(
    response: Response,
    guid: uuid.UUID | None,
    data: ConsentInput | None = None
):
    if not guid:
        guid = uuid.uuid4()
    response.set_cookie(
        key="guid",
        value=guid,
        max_age=60 * 60 * 24 * 7,
        samesite="none",
        secure=True,
        httponly=True
    )
    user = user_data.setdefault(
        guid,
        {"tracking": False, "not_tracking": False}
    )
    if data:
        user.update(dict(data))
    scripts = set()
    denied = set()
    for cat, val in user.items():
        if val:
            scripts |= script_data[cat]
        else:
            denied |= script_data[cat]
    print(scripts)
    print(denied)
    return user, scripts - denied


@app.get("/api/get")
async def fetch_consent(
    response: Response,
    guid: uuid.UUID | None = Cookie(None),
):
    user, scripts = handle(response, guid)
    return {"consent": user, "scripts": scripts}


@app.post("/api/set")
async def set_consent(
    consent: ConsentInput,
    response: Response,
    guid: uuid.UUID | None = Cookie(None),
):
    user, scripts = handle(response, guid, consent)
    return {"consent": user, "scripts": scripts}