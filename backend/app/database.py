import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load .env from backend directory
base_dir = os.path.dirname(os.path.dirname(__file__))
dotenv_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=dotenv_path)

DB_USER = os.getenv("DB_USER", "workshop")
DB_PASS = os.getenv("DB_PASSWORD", "workshoppass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "workshopdb")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

def wait_for_db(retries=5, delay=2):
    for i in range(retries):
        try:
            engine = create_engine(DATABASE_URL)
            conn = engine.connect()
            conn.close()
            return
        except Exception as e:
            print(f"DB not ready yet ({i+1}/{retries}): {e}")
            time.sleep(delay)
    print("Warning: database may not be ready. Continuing anyway.")

wait_for_db()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()