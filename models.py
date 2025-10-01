from typing import Optional
from sqlmodel import Field, SQLModel

# Modelo Base para crear y actualizar tareas (no incluye el ID)
class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)

# Modelo de la base de datos (incluye ID y metadatos de tabla)
class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Modelo de lectura (incluye el ID para las respuestas)
class TaskRead(TaskBase):
    id: int