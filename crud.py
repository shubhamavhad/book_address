from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import models
import schemas
import math
import logging

logger = logging.getLogger("address-book.crud")

#Create address
def create_address(db: Session, address: schemas.AddressCreate):
    try:
        db_address = models.Address(**address.model_dump())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Database error while creating address")
        raise e


#get all addresses
def get_addresses(db: Session):
    return db.query(models.Address).all()

#Update the address
def update_address(db: Session, address_id: int, address_update: schemas.AddressUpdate):
    try:
        db_address = db.query(models.Address).filter(
            models.Address.id == address_id
        ).first()

        if not db_address:
            return None

        update_data = address_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_address, key, value)

        db.commit()
        db.refresh(db_address)
        return db_address

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Database error during update")
        raise e

#Delete address
def delete_address(db: Session, address_id: int):
    address = db.query(models.Address).filter(
        models.Address.id == address_id
    ).first()

    if address:
        db.delete(address)
        db.commit()

    return address


#Get nearby addresses
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + \
        math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
