from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


# City database model
class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key= True, index= True)
    name = Column(String(20), unique=True, index= True, nullable= False)
    is_active = Column(Boolean, default= True)

    city_products = relationship("CityProduct", back_populates="city")

# Category database model
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key= True, index= True)
    name = Column(String(30), unique=True, index= True, nullable= False)
    description = Column(String(100), nullable= False)
    is_active = Column(Boolean, default= True)
    created_at = Column(DateTime, default=datetime.now)

    products = relationship("Product", back_populates="category")


# Product database model
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, index=True, nullable=False)
    description = Column(String(100), nullable=False)
    price = Column(Float, default=0.0, nullable=False)
    image_url = Column(String(500), nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category",back_populates="products")

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    city_products = relationship("CityProduct", back_populates="product")

# City product mapping database model
class CityProduct(Base):
    __tablename__ = "cityproducts"

    id = Column(Integer, primary_key= True, index= True)

    city_id = Column(Integer, ForeignKey("cities.id"), nullable= False) 
    product_id = Column(Integer, ForeignKey("products.id"), nullable= False)

    is_available = Column(Boolean, default= True)
    created_at = Column(DateTime, default= datetime.now)

    city = relationship("City", back_populates="city_products")

    product = relationship("Product", back_populates="city_products")

    __table_args__ = (
        UniqueConstraint(
            "city_id",
            "product_id",
            name="unique_city_product"
        ),
    )
    
    
