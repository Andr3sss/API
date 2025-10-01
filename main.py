
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

# Importar funciones de conexión y modelos
from database import create_db_and_tables, get_session
from models import User, UserBase, Product, ProductBase

# Inicialización de la API
app = FastAPI(
    title="FastAPI RDS App",
    version="2.0.0"
)

# Ejecutar la función para crear las tablas al iniciar la aplicación
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the RDS-powered FastAPI! Access /docs."}

# --- RUTAS CRUD PARA USUARIOS ---

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(*, session: Session = Depends(get_session), user: UserBase):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[User])
def read_all_users(*, session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@app.get("/users/{user_id}", response_model=User)
def read_single_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(*, session: Session = Depends(get_session), user_id: int, user_update: UserBase):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Aplicar la actualización
    updated_data = user_update.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(updated_data)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    return