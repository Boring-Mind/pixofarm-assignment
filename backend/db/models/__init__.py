from db.config import BaseModel
from sqlalchemy import Column, Integer, Float, ForeignKey, Text, DateTime


class Continent(BaseModel):
    __tablename__ = "continent"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    # Hex representation of continents' color for frontend
    color = Column(Text, nullable=False, unique=True)


class Temperature(BaseModel):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    temperature = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    city = Column(
        Integer,
        ForeignKey("city.id"),
        nullable=False,
    )


class City(BaseModel):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)
    continent = Column(
        Integer,
        ForeignKey("continent.id"),
        nullable=False,
    )
