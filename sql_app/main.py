from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/pets/{name}', response_model=schemas.Pet)
def get_pet(name: str, db: Session = Depends(get_db)):
    pet = crud.get_pet_by_name(db, name)
    if not pet:
        raise HTTPException(
            status_code=200, detail=f'There is no pet with name {name}')
    else:
        return pet


@app.get('/pets/', response_model=list[schemas.Pet])
def read_pets(type: str, db: Session = Depends(get_db)):
    pets = crud.get_pets(db, type_=type)
    return pets


@app.delete('/pets/{name}')
def delete_pet(name: str, db: Session = Depends(get_db)):
    result = crud.delete_pet(db, name)
    if result:
        return {'detail': f'Successfully deleted pet with name {name}'}
    else:
        raise HTTPException(
            status_code=404, detail=f'No such pet with name {name}')


@app.delete('/pets/')
def delete_pets(type: str, db: Session = Depends(get_db)):
    amount = crud.delete_pets(db, type)
    if amount:
        return {'detail': f'Successfully deleted {amount} pets with type {type}'}
    else:
        raise HTTPException(
            status_code=404, detail=f'No such pet with pet type {type}')


@app.post('/pets/', status_code=201)
def create_pet(pet: schemas.Pet, db: Session = Depends(get_db)):
    db_pet = crud.get_pet_by_name(db, pet.name)
    if db_pet:
        raise HTTPException(
            status_code=422, detail=f'There is already a pet with name {pet.name}')
    crud.create_pet(db, pet)
    return {'detail': f'Successfully created pet with name {pet.name}'}
