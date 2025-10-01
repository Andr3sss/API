import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from models import Task # Solo importamos el nuevo modelo Task

# Cargar variables de entorno del archivo .env (solo para desarrollo local)
load_dotenv()

# --- Configuración de Conexión ---

SQLITE_FILE_NAME = "database.db"
LOCAL_DB_URL = f"sqlite:///{SQLITE_FILE_NAME}"

# Usará la variable DATABASE_URL de .env o el valor exportado en EC2
DATABASE_URL = os.getenv("DATABASE_URL") or LOCAL_DB_URL 

# Crear el engine (objeto de conexión a RDS o SQLite)
engine = create_engine(DATABASE_URL, echo=False)


# --- Funciones de Utilidad ---

def create_db_and_tables():
    """Asegura que la tabla Task exista en la DB."""
    # Nota: SQLModel creará la tabla 'task' en tu RDS la primera vez que se ejecute.
    SQLModel.metadata.create_all(engine)

def get_session():
    """Función de dependencia de FastAPI que gestiona la sesión de la base de datos."""
    with Session(engine) as session:
        yield session