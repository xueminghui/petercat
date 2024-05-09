import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from uilts.env import get_env_variable


# Import fastapi routers
from routers import bot, health_checker, github, rag, auth, chat


is_dev = bool(get_env_variable("IS_DEV"))
session_secret_key = get_env_variable("FASTAPI_SECRET_KEY")
app = FastAPI( 
    title="Bo-meta Server",
    version="1.0",
    description="Agent Chat APIs"
)

app.add_middleware(
    SessionMiddleware,
    secret_key = session_secret_key,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(health_checker.router)
app.include_router(github.router)
app.include_router(rag.router)
app.include_router(bot.router)
app.include_router(auth.router)
app.include_router(chat.router)

if __name__ == "__main__":
    if is_dev:
        uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), reload=True)
    else:
        uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
