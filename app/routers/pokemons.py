
import os
from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models, app.schemas as schemas

router = APIRouter(prefix="/pokemons", tags=["pokemons"])

auth_scheme = HTTPBearer()

TOKEN_SECRETO = os.getenv("API_TOKEN")

def validar_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    print(token,'tokentokentokentokentokentoken')
    if token.credentials != TOKEN_SECRETO:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token.credentials

@router.get("/", response_model=schemas.PaginatedPokemon)
def get_pokemons(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    total_records = db.query(models.Pokemon).count()
    
    pokemons = db.query(models.Pokemon).offset(skip).limit(limit).all()
    
    current_page = (skip // limit) + 1
    
    return {
        "total": total_records,
        "page": current_page,
        "limit": limit,
        "results": pokemons
    }

@router.post("/", response_model=schemas.Pokemon, dependencies=[Depends(validar_token)])
def create_pokemon(pokemon: schemas.PokemonCreate, db: Session = Depends(get_db)):
    nuevo_pokemon = models.Pokemon(
        nombre=pokemon.nombre, 
        tipo=pokemon.tipo, 
        nivel=pokemon.nivel,
        foto_url=pokemon.foto_url, 
        poder=pokemon.poder,       
        peso=pokemon.peso          
    )
    db.add(nuevo_pokemon)
    db.commit()
    db.refresh(nuevo_pokemon)
    return nuevo_pokemon


@router.put("/{pokemon_id}", response_model=schemas.Pokemon, dependencies=[Depends(validar_token)])
def update_pokemon(
    pokemon_id: int, 
    pokemon_update: schemas.PokemonCreate, 
    db: Session = Depends(get_db)
):
    db_pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()
    
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")

    db_pokemon.nombre = pokemon_update.nombre
    db_pokemon.tipo = pokemon_update.tipo
    db_pokemon.nivel = pokemon_update.nivel
    db_pokemon.foto_url = pokemon_update.foto_url
    db_pokemon.poder = pokemon_update.poder
    db_pokemon.peso = pokemon_update.peso

    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon

@router.delete("/{pokemon_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(validar_token)])
def delete_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    db_pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()
    
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")

    db.delete(db_pokemon)
    db.commit()
    return None 