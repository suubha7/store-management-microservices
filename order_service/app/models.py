from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key= True, index= True)
    user_id = Column(Integer, nullable= False)
    product_id = Column(Integer, nullable= False)
    city_id = Column(Integer, nullable=False)
    quantity = Column(Integer, default= 1)
    
    created_at = Column(DateTime, default= datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "product_id",
            "city_id",
            name="unique_user_product_cart"
        ),
    )

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key= True, index= True)
    user_id = Column(Integer, nullable= False)
    city_id = Column(Integer, nullable= False)
    total_amount = Column(Float, default=0.0)
    status = Column(String(20), nullable=False, default="pending")

    created_at = Column(DateTime, default= datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

class OrderItem(Base):
    __tablename__ = "orderitems"

    id = Column(Integer, primary_key= True, index= True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, nullable= False)
    product_name = Column(String, nullable= False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default= 1)
    subtotal = Column(Float, nullable=False)

    order = relationship(
        "Order",
        back_populates="order_items"
    )