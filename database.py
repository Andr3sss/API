
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from models import User, Product  

load_dotenv()


SQLITE_FILE_NAME = "database.db"
LOCAL_DB_URL = f"sqlite:///{SQLITE_FILE_NAME}"


DATABASE_URL = os.getenv("DATABASE_URL") or LOCAL_DB_URL


engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():

    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session