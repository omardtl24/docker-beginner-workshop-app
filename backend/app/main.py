# backend/app/main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from .database import SessionLocal, engine
from . import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workshop API")


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