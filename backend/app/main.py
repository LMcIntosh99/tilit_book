"""
FastAPI application setup.

- Creates database tables on startup.
- Configures CORS middleware.
- Includes the comments router.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import comments
from . import models
from .database import get_engine

app = FastAPI()


# Create all tables on startup defined by the ORM models (if they don't exist)
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=get_engine())


# Configure CORS to allow frontend requests from localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the comments API routes
app.include_router(comments.router)
