from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Inventory
from app.schema.inventory_schema import CreateInventory, InventoryStockUpdate, InventoryResponse
from app.dependencies import require_admin

inventory_router = APIRouter(prefix="/admin", tags=["Admin Inventory APIs"], dependencies=[Depends(require_admin)])

@inventory_router.get("/inventories", response_model=list[InventoryResponse], status_code=status.HTTP_200_OK)
def get_inventories(db: Session= Depends(get_db)):
    inventories = db.query(Inventory).all()

    return inventories

@inventory_router.post("/inventories", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory(inventory_data: CreateInventory, db: Session = Depends(get_db)):

    inventory = db.query(Inventory).filter(Inventory.city_id == inventory_data.city_id, 
                                                Inventory.product_id == inventory_data.product_id).first()
    
    if inventory:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The Product is already assign to the city")
    
    new_inventory = Inventory(city_id= inventory_data.city_id, product_id= inventory_data.product_id, stock_quantity= inventory_data.stock_quantity)

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return new_inventory

@inventory_router.get("/inventories/{inventory_id}", response_model=InventoryResponse)
def get_inventory_by_id(inventory_id: int, db: Session = Depends(get_db)):
    
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()

    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")

    return inventory

@inventory_router.put("/inventories/{inventory_id}",response_model=InventoryResponse, status_code=status.HTTP_200_OK)
def update_inventory_stock(inventory_id: int, inventory_data: InventoryStockUpdate, db: Session = Depends(get_db)):
    
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()

    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")

    inventory.stock_quantity = inventory_data.stock_quantity

    db.commit()
    db.refresh(inventory)

    return inventory

@inventory_router.delete("/inventories/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()

    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")

    db.delete(inventory)
    db.commit()

