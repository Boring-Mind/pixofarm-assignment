from sqlalchemy import Column, Integer, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from db.config import BaseModel


class Continent(BaseModel):
    __tablename__ = "continent"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    # Hex representation of continents' color for frontend
    color = Column(Text, nullable=False, unique=True)
    cities = relationship("City", back_populates="continent")


class Temperature(BaseModel):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    min = Column(Float, nullable=False)
    max = Column(Float, nullable=False)
    mean = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    city_id = Column(
        Integer,
        ForeignKey("city.id"),
        nullable=False,
    )
    city = relationship("City", back_populates="temperatures")


class City(BaseModel):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)
    continent_id = Column(
        Integer,
        ForeignKey("continent.id"),
        nullable=False,
    )
    continent = relationship("Continent", back_populates="cities")
    temperatures = relationship("Temperature", back_populates="city")
