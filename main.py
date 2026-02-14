from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
import schemas
import crud
from database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

logger = logging.getLogger("address-book-app.main")


# Db dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Create address
@app.post("/addresses/")
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    try:
        logger.info("POST /addresses - Creating address")

        result = crud.create_address(db, address)

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "data": {
                    "id": result.id,
                    "name": result.name,
                    "street": result.street,
                    "city": result.city,
                    "latitude": result.latitude,
                    "longitude": result.longitude,
                }
            }
        )

    except SQLAlchemyError as e:
        logger.exception("Database error while creating address")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Database error occurred",
                "details": str(e)
            }
        )

    except Exception as e:
        logger.exception("Unexpected error while creating address")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "details": str(e)
            }
        )


# Get all addresses
@app.get("/addresses/")
def read_addresses(db: Session = Depends(get_db)):
    try:
        logger.info("GET /addresses - Fetching all addresses")

        result = crud.get_addresses(db)

        data = [
            {
                "id": addr.id,
                "name": addr.name,
                "street": addr.street,
                "city": addr.city,
                "latitude": addr.latitude,
                "longitude": addr.longitude,
            }
            for addr in result
        ]

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "count": len(data),
                "data": data
            }
        )

    except SQLAlchemyError as e:
        logger.exception("Database error while fetching addresses")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Database error occurred",
                "details": str(e)
            }
        )

    except Exception as e:
        logger.exception("Unexpected error while fetching addresses")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "details": str(e)
            }
        )


#Update address
@app.put("/addresses/{address_id}")
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    try:
        updated = crud.update_address(db, address_id, address)

        if not updated:
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Address not found"}
            )

        return JSONResponse(
            status_code=200,
            content={"success": True, "data": "Address updated successfully"}
        )

    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Database error occured", "details": str(e)}
        )
    except Exception as e:
        logger.exception("Unexpected error while updateing address")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "details": str(e)
            }
        )



#Delete address
@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"DELETE /addresses/{address_id}")

        deleted = crud.delete_address(db, address_id)

        if not deleted:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "Address not found"
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Address deleted successfully"
            }
        )

    except SQLAlchemyError as e:
        logger.exception("Database error while deleting address")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Database error occurred",
                "details": str(e)
            }
        )

    except Exception as e:
        logger.exception("Unexpected error while deleting address")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "details": str(e)
            }
        )


#Get nearby addresses
@app.get("/addresses/nearby/")
def get_nearby(lat: float, lon: float, distance: float, db: Session = Depends(get_db)):
    try:
        logger.info(
            f"GET /addresses/nearby - lat={lat}, lon={lon}, distance={distance}"
        )

        if distance <= 0:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Distance must be greater than 0"
                }
            )

        if not (-90 <= lat <= 90):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Latitude must be between -90 and 90"
                }
            )

        if not (-180 <= lon <= 180):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Longitude must be between -180 and 180"
                }
            )
        

        #get the addresses
        addresses = crud.get_addresses(db)
        nearby = []

        for addr in addresses:
            dist = crud.calculate_distance(lat, lon, addr.latitude, addr.longitude)
            if dist <= distance:
                nearby.append({
                    "id": addr.id,
                    "name": addr.name,
                    "street": addr.street,
                    "city": addr.city,
                    "latitude": addr.latitude,
                    "longitude": addr.longitude,
                })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "count": len(nearby),
                "data": nearby
            }
        )

    except SQLAlchemyError as e:
        logger.exception("Database error while searching nearby addresses")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Database error occurred",
                "details": str(e)
            }
        )

    except Exception as e:
        logger.exception("Unexpected error while searching nearby addresses")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "details": str(e)
            }
        )
