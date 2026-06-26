from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_admin

from app.models import Category
from app.schema.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryStatusUpdate

category_router = APIRouter(prefix="/admin", tags=["Admin Categories"], dependencies=[Depends(require_admin)])

# Retrieve all categories
@category_router.get("/categories", response_model=list[CategoryResponse])
def get_categories(db: Session= Depends(get_db)):
    categories = db.query(Category).all()

    return categories

# Retrieve category details by ID
@category_router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")    

    return category

# Create a new category
@category_router.post("/categories", response_model= CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):

    category = category_data.name.strip().title()

    existing_category = db.query(Category).filter(Category.name == category_data.name).first()
    if existing_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exist.")
    
    new_category = Category(name = category, description = category_data.description)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

# Update category details
@category_router.put("/categories/{category_id}", response_model= CategoryResponse, status_code=status.HTTP_200_OK)
def update_category_by_id(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    if category_data.name != None:
        category.name = category_data.name.strip().title()
    if category_data.description != None:
        category.description = category_data.description
        

    db.commit()
    db.refresh(category)

    return category

# Update category status
@category_router.put("/categories/{category_id}/status", response_model= CategoryResponse, status_code=status.HTTP_200_OK)
def update_category_status(category_id: int, category_data: CategoryStatusUpdate, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    category.is_active = category_data.is_active

    db.commit()
    db.refresh(category)

    return category

