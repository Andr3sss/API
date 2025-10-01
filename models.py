# models.py

from typing import Optional
from sqlmodel import Field, SQLModel

# Clase Base: Define los campos comunes para las peticiones/respuestas
class UserBase(SQLModel):
    name: str
    email: str
    
# Clase Tabla: Hereda de Base y añade metadatos de DB (primary key, table=True)
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Clase Base para Productos
class ProductBase(SQLModel):
    name: str
    price: float
    description: Optional[str] = None

# Clase Tabla para Productos
class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)