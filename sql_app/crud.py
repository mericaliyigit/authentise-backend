from sqlalchemy.orm import Session

from . import models, schemas


def create_pet(db: Session, pet: schemas.Pet):
    db_pet = models.Pet(
        name=pet.name,
        breed=pet.breed,
        rank=pet.rank,
        type=pet.type,
        img_url=pet.img_url
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def get_pet_by_name(db: Session, name: str):
    return db.query(models.Pet).filter(models.Pet.name == name).one_or_none()


def get_pets(db: Session, type_: str):
    return db.query(models.Pet).filter(models.Pet.type == type_).order_by(models.Pet.rank.desc()).all()


def delete_pet(db: Session, name: str):
    the_pet = db.query(models.Pet).filter(
        models.Pet.name == name).one_or_none()
    if the_pet:
        db.delete(the_pet)
        db.commit()
        return True
    return False


def delete_pets(db: Session, type_: str):
    query = db.query(models.Pet).filter(models.Pet.type == type_)
    count = query.count()
    query.delete()
    db.commit()
    return count
