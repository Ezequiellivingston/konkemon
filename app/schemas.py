from pydantic import BaseModel
from typing import List, Optional

class PokemonBase(BaseModel):
    nombre: str
    tipo: str
    nivel: int = 1
    foto_url: Optional[str] = None
    poder: int = 0
    peso: float = 0.0

class PokemonCreate(PokemonBase):
    pass

class Pokemon(PokemonBase):
    id: int

    class Config:
        from_attributes = True

class PaginatedPokemon(BaseModel):
    total: int
    page: int
    limit: int
    results: List[Pokemon]