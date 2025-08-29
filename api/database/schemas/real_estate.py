import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
)

from database.database import Base


class SellMedianPrice(Base):
    __tablename__ = "sell_median_price"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prix_median_m2 = Column(Integer, nullable=False)
    evolution_one_year = Column(Integer, nullable=True)
    evolution_five_years = Column(Integer, nullable=True)


class RentMedianPrice(Base):
    __tablename__ = "rent_median_price"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prix_median_m2 = Column(Integer, nullable=False)
    evolution_one_year = Column(Integer, nullable=True)
    evolution_five_years = Column(Integer, nullable=True)


class SellMedianPriceByRoom(Base):
    __tablename__ = "sell_median_price_by_room"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_1 = Column(Integer, nullable=True)
    room_2 = Column(Integer, nullable=True)
    room_3 = Column(Integer, nullable=True)
    room_4 = Column(Integer, nullable=True)
    room_5 = Column(Integer, nullable=True)
    room_6 = Column(Integer, nullable=True)
    room_7 = Column(Integer, nullable=True)


class RentMedianPriceByRoom(Base):
    __tablename__ = "rent_median_price_by_room"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_1 = Column(Integer, nullable=True)
    room_2 = Column(Integer, nullable=True)
    room_3 = Column(Integer, nullable=True)
    room_4 = Column(Integer, nullable=True)
    room_5 = Column(Integer, nullable=True)
    room_6 = Column(Integer, nullable=True)
    room_7 = Column(Integer, nullable=True)


class Appartment(Base):
    __tablename__ = "appartment_data"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sell_median_price = Column(
        Integer,
        ForeignKey("sell_median_price.id", ondelete="CASCADE"),
    )
    rent_median_price = Column(
        Integer,
        ForeignKey("rent_median_price.id", ondelete="CASCADE"),
    )
    sell_median_price_by_room = Column(
        Integer,
        ForeignKey("sell_median_price_by_room.id", ondelete="CASCADE"),
    )
    rent_median_price_by_room = Column(
        Integer,
        ForeignKey("rent_median_price_by_room.id", ondelete="CASCADE"),
    )


class House(Base):
    __tablename__ = "house_data"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sell_median_price = Column(
        Integer,
        ForeignKey("sell_median_price.id", ondelete="CASCADE"),
    )
    rent_median_price = Column(
        Integer,
        ForeignKey("rent_median_price.id", ondelete="CASCADE"),
    )
    sell_median_price_by_room = Column(
        Integer,
        ForeignKey("sell_median_price_by_room.id", ondelete="CASCADE"),
    )
    rent_median_price_by_room = Column(
        Integer,
        ForeignKey("rent_median_price_by_room.id", ondelete="CASCADE"),
    )


class TownRealEstate(Base):
    __tablename__ = "real_estate"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    country_id = Column(String, nullable=True)
    region_id = Column(String, nullable=True)
    region_name = Column(String, nullable=False)
    department_id = Column(String, nullable=True)
    department_name = Column(String, nullable=False)
    postal_code = Column(String, unique=True, nullable=False)
    city_label = Column(String, unique=True, nullable=True)
    city = Column(String, unique=True, nullable=False)
    zipcode = Column(String, nullable=False)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    source = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    is_shape = Column(Boolean, default=False)
    appartment_data = Column(
        Integer, ForeignKey("appartment_data.id", ondelete="CASCADE"), nullable=True
    )
    house_data = Column(
        Integer, ForeignKey("house_data.id", ondelete="CASCADE"), nullable=True
    )
