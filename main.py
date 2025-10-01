# main.py

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

# --- SCHEMAS (MODELOS DE DATOS) ---

class BaseItem(BaseModel):
    name: str

class User(BaseItem):
    id: Optional[int] = None
    email: str

class Product(BaseItem):
    id: Optional[int] = None
    price: float
    description: Optional[str] = None

# --- DATOS EN MEMORIA (SIMULACIÓN DE DB) ---

fake_users_db: List[User] = []
user_counter = 0

fake_products_db: List[Product] = []
product_counter = 0

# --- INICIALIZACIÓN DE LA API ---

app = FastAPI(
    title="API EC2 Deployment Demo",
    version="1.0.0"
)

# --- RUTA RAÍZ ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the API! Access /docs for endpoints."}

# --- RUTAS CRUD PARA USUARIOS ---

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    global user_counter
    user_counter += 1
    new_user = user.model_copy(update={"id": user_counter}) 
    fake_users_db.append(new_user)
    return new_user

@app.get("/users/", response_model=List[User])
def read_all_users():
    return fake_users_db

@app.get("/users/{user_id}", response_model=User)
def read_single_user(user_id: int):
    for user in fake_users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    for index, stored_user in enumerate(fake_users_db):
        if stored_user.id == user_id:
            updated_user = user.model_copy(update={"id": user_id})
            fake_users_db[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    global fake_users_db
    initial_length = len(fake_users_db)
    fake_users_db = [user for user in fake_users_db if user.id != user_id]
    
    if len(fake_users_db) == initial_length:
        raise HTTPException(status_code=404, detail="User not found")
    return

# --- RUTAS CRUD PARA PRODUCTOS ---

@app.post("/products/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    global product_counter
    product_counter += 1
    new_product = product.model_copy(update={"id": product_counter})
    fake_products_db.append(new_product)
    return new_product

@app.get("/products/", response_model=List[Product])
def read_all_products():
    return fake_products_db

@app.get("/products/{product_id}", response_model=Product)
def read_single_product(product_id: int):
    for product in fake_products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    for index, stored_product in enumerate(fake_products_db):
        if stored_product.id == product_id:
            updated_product = product.model_copy(update={"id": product_id})
            fake_products_db[index] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    global fake_products_db
    initial_length = len(fake_products_db)
    fake_products_db = [product for product in fake_products_db if product.id != product_id]
    
    if len(fake_products_db) == initial_length:
        raise HTTPException(status_code=404, detail="Product not found")
    return