from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import comments

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(comments.router)
