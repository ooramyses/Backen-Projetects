from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import random
import string

DATABASE_URL = "sqlite:///./shortener.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    original = Column(String)
    short = Column(String, unique=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shorten")
def shorten_url(original_url: str):
    db = SessionLocal()
    code = generate_code()

    new_url = URL(original=original_url, short=code)
    db.add(new_url)
    db.commit()
    db.close()

    return {"short_url": f"http://localhost:8000/{code}"}

@app.get("/{code}")
def redirect(code: str):
    db = SessionLocal()
    url = db.query(URL).filter(URL.short == code).first()
    db.close()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return {"original_url": url.original}
