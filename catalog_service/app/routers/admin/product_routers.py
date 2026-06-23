from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db

from app.models import Product
from app.schema.product import ProductCreate, ProductUpdate, ProductResponse, ProductStatusUpdate

product_router = APIRouter(prefix="/admin", tags=["Admin Products"])

@product_router.get("/products",response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return products


@product_router.get("/products/{product_id}",response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return product

@product_router.post("/products", response_model= ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):

    product = product_data.name.strip().title()

    existing_product = db.query(Product).filter(Product.name == product_data.name).first()
    if existing_product:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exist.")
    
    new_product = Product(name = product, description = product_data.description, price = product_data.price, category_id = product_data.category_id)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@product_router.put("/products/{product_id}", response_model= ProductResponse, status_code=status.HTTP_200_OK)
def update_product_by_id(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product_data.name != None:
        product.name = product_data.name.strip().title()
    if product_data.description != None:
        product.description = product_data.description
    if product_data.price != None:
        product.price = product_data.price
    if product_data.category_id != None:
        product.category_id = product_data.category_id

    db.commit()
    db.refresh(product)

    return product
     
@product_router.put("/products/{product_id}/status", response_model= ProductResponse, status_code=status.HTTP_200_OK)
def update_product_status(product_id: int, product_data: ProductStatusUpdate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product.is_active = product_data.is_active
    
    db.commit()
    db.refresh(product)

    return product