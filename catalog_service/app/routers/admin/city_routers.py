from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import City
from app.schema.city import CityCreate, CityStatusUpdate, CityResponse
from app.dependencies import require_admin


city_router = APIRouter(prefix="/admin", tags=["Admin Cities"], dependencies=[Depends(require_admin)])

# Retrieve all cities
@city_router.get("/cities", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    cities = db.query(City).all()

    return cities

# Retrieve city details by ID
@city_router.get("/cities/{city_id}", response_model=CityResponse)
def get_city_by_id(city_id: int, db: Session = Depends(get_db)):

    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    
    return city

# Create a new city
@city_router.post("/city", response_model= CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(city_data: CityCreate, db: Session = Depends(get_db)):

    city_name = city_data.name.strip().title()

    existing_city = db.query(City).filter(City.name == city_name).first()
    if existing_city:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="City already exist.")
    
    new_city = City(name = city_name)

    db.add(new_city)
    db.commit()
    db.refresh(new_city)

    return new_city

    
# Update city status
@city_router.put("/city/{city_id}/status", response_model= CityResponse, status_code=status.HTTP_200_OK)
def update_city_status(city_id: int, city_data: CityStatusUpdate, db: Session = Depends(get_db)):


    city = db.query(City).filter(City.id == city_id).first()

    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    
    city.is_active = city_data.is_active

    db.commit()
    db.refresh(city)

    return city

