from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers.users import router as users_router
from app.routers.pokemons import router as pokemons_router

app = FastAPI()

Base.metadata.create_all(bind=engine)  # crea tablas

app.include_router(pokemons_router)