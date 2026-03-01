from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo = Column(String)
    nivel = Column(Integer, default=1)
    
    # --- ACÁ ESTÁN LOS QUE FALTABAN ---
    foto_url = Column(String, nullable=True)
    poder = Column(Integer, default=0)
    peso = Column(Float, default=0.0)