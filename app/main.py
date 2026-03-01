from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routers.users import router as users_router
from app.routers.pokemons import router as pokemons_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],              
)

Base.metadata.create_all(bind=engine)  

app.include_router(pokemons_router)