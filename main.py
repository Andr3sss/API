from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional

from database import create_db_and_tables, get_session
from models import Task, TaskBase, TaskRead

# --- Configuración de la API ---

app = FastAPI(
    title="ToDo App API (RDS)",
    version="3.0.0"
)

# --- Configuración CORS (CRÍTICO para React) ---
# Permite que cualquier origen ("*") acceda a tu API.
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Evento de Inicio ---

@app.on_event("startup")
def on_startup():
    """Crea la tabla Task al iniciar la aplicación."""
    create_db_and_tables()

# --- Rutas CRUD para Task ---

@app.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(*, session: Session = Depends(get_session), task: TaskBase):
    """POST /tasks → Crea una tarea."""
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[TaskRead])
def read_all_tasks(*, session: Session = Depends(get_session)):
    """GET /tasks → Lista todas las tareas."""
    tasks = session.exec(select(Task)).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskRead)
def read_single_task(*, session: Session = Depends(get_session), task_id: int):
    """GET /tasks/{id} → Consulta una tarea por ID."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(*, session: Session = Depends(get_session), task_id: int, task_update: TaskBase):
    """PUT /tasks/{id} → Actualiza título, descripción o estado de la tarea."""
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Aplicar la actualización
    updated_data = task_update.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(updated_data)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(*, session: Session = Depends(get_session), task_id: int):
    """DELETE /tasks/{id} → Elimina una tarea."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return