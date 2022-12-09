from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infra.sqlalchemy.config.database import criar_bd
from src.routes import routes_auth


# criar_bd()

app = FastAPI()

origins = ['http://127.0.0.1:5501']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_auth.router, prefix="/auth")