# backend/app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from .database import SessionLocal, engine
from . import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workshop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods (GET, POST, OPTIONS, etc)
    allow_headers=["*"],
)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/person/", response_model=schemas.Person)
def create_person(person: schemas.Person, db: Session = Depends(get_db)):
    db_person = models.Person(name=person.name, email=person.email, age=person.age)
    db.add(db_person)
    try:
        db.commit()
        db.refresh(db_person)
        return db_person
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Person with this email already exists")


@app.get("/people/", response_model=List[schemas.Person])
def list_people(db: Session = Depends(get_db)):
    items = db.query(models.Person).all()
    return [schemas.Person.from_orm(p) for p in items]


@app.delete("/people/", response_model=dict)
def clear_people(db: Session = Depends(get_db)):
    deleted = db.query(models.Person).delete()
    db.commit()
    return {"deleted": deleted, "detail": "All people removed"}
