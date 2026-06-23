from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import City, Category, Product, CityProduct
from app.schema.city import CityResponse
from app.schema.product import ProductResponse
from app.schema.category import CategoryResponse


catalog_router = APIRouter(prefix='/catalog', tags=["Catalog APIs"])

@catalog_router.get("/cities", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    cities = db.query(City).filter(City.is_active == True).all()

    return cities

@catalog_router.get("/cities/{city_id}/categories", response_model= list[CategoryResponse])
def get_categories_by_city_id(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()

    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    
    categories = (
        db.query(Category)
        .join(Product, Product.category_id == Category.id)
        .join(CityProduct, CityProduct.product_id == Product.id)
        .filter(
            CityProduct.city_id == city_id,
            CityProduct.is_available == True,
            Product.is_active == True,
            Category.is_active == True
        )
        .distinct()
        .all()
    )

    return categories
    

@catalog_router.get("/cities/{city_id}/products", response_model=list[ProductResponse])
def get_products_by_city_id(city_id: int, db: Session = Depends(get_db)):
    
    city = db.query(City).filter(City.id == city_id, City.is_active == True).first()

    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    
    products = (
        db.query(Product)
        .join(CityProduct, CityProduct.product_id == Product.id)
        .join(Category, Category.id == Product.category_id)
        .filter(
            CityProduct.city_id == city_id,
            CityProduct.is_available == True,
            Product.is_active == True,
            Category.is_active == True
        )
        .all()
    )

    return products


@catalog_router.get("/cities/{city_id}/products/category/{category_id}", response_model=list[ProductResponse])
def get_products_by_category_id(city_id: int, category_id: int, db: Session = Depends(get_db)):

    city = db.query(City).filter(City.id == city_id, City.is_active == True).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    
    category = db.query(Category).filter(Category.id == category_id, Category.is_active == True).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    products = (
        db.query(Product)
        .join(CityProduct, CityProduct.product_id == Product.id)
        .filter(
            CityProduct.city_id == city_id,
            CityProduct.is_available == True,
            Product.category_id == category_id,
            Product.is_active == True
        )
        .all()
    )

    return products


@catalog_router.get("/products/{product_id}", response_model=ProductResponse)
def get_product_by_product_id(product_id: int, db: Session = Depends(get_db)):

    product = (
        db.query(Product)
        .join(Category, Category.id == Product.category_id)
        .filter(
            Product.id == product_id,
            Product.is_active == True,
            Category.is_active == True
        )
        .first()
    )

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return product