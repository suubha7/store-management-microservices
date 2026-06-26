from sqlalchemy import Column, Integer, DateTime, UniqueConstraint
from datetime import datetime
from app.database import Base

# Inventory database model
class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, nullable= False)
    product_id = Column(Integer, nullable= False)
    stock_quantity = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint(
            "city_id",
            "product_id",
            name="unique_city_product_inventory"
        ),
    )