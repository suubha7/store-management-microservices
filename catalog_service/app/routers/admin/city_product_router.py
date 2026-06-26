from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CityProduct, City, Product
from app.schema.city_product import CityProductCreate, CityProductResponse, CityProductAvailabilityUpdate
from app.dependencies import require_admin

city_product_router = APIRouter(prefix="/admin", tags=["Admin City Products"], dependencies=[Depends(require_admin)])


# Map a product to a city
@city_product_router.post("/city-products", response_model= CityProductResponse, status_code=status.HTTP_201_CREATED)
def create_city_product(city_product_data: CityProductCreate, db: Session= Depends(get_db)):

    city = db.query(City).filter(City.id == city_product_data.city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    product = db.query(Product).filter(Product.id == city_product_data.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    existing_city_product = db.query(CityProduct).filter(CityProduct.city_id == city_product_data.city_id, CityProduct.product_id == city_product_data.product_id).first()
    if existing_city_product:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product is already assigned to this city")
   
    new_city_product = CityProduct(city_id = city_product_data.city_id, product_id = city_product_data.product_id)
    db.add(new_city_product)
    db.commit()
    db.refresh(new_city_product)

    return new_city_product


# Retrieve all city product mappings
@city_product_router.get("/city-products",response_model=list[CityProductResponse])
def get_city_products(db: Session = Depends(get_db)):
    city_products = db.query(CityProduct).all()

    return city_products


# Retrieve city product details by ID
@city_product_router.get("/city-products/{city_product_id}", response_model=CityProductResponse)
def get_city_product_by_id(city_product_id: int, db: Session = Depends(get_db)):

    city_product = db.query(CityProduct).filter( CityProduct.id == city_product_id).first()

    if not city_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="City product assignment not found")

    return city_product

# Update product availability in city
@city_product_router.put("/city-products/{city_product_id}/availability", 
                         response_model=CityProductResponse, 
                         status_code=status.HTTP_200_OK)
def update_city_product_availability(city_product_id: int, 
                                     city_product_data: CityProductAvailabilityUpdate,
                                     db: Session = Depends(get_db)
                                    ):
    
    city_product = db.query(CityProduct).filter(CityProduct.id == city_product_id).first()

    if not city_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City product assignment not found")

    city_product.is_available = city_product_data.is_available

    db.commit()
    db.refresh(city_product)

    return city_product

# Delete city product mapping
@city_product_router.delete("/city-products/{city_product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city_product(city_product_id: int, db: Session = Depends(get_db)):
    city_product = db.query(CityProduct).filter(CityProduct.id == city_product_id).first()

    if not city_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City product assignment not found")

    db.delete(city_product)
    db.commit()