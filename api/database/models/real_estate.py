from datetime import datetime
from xmlrpc.client import boolean
from pydantic import BaseModel
from sqlalchemy.engine import RowMapping


class SellMedianPriceData(BaseModel):
    prix_median_m2: int | None
    evolution_one_year: int | None
    evolution_five_years: int | None


class RentMedianPriceData(BaseModel):
    prix_median_m2: int | None = None
    evolution_one_year: int | None = None
    evolution_five_years: int | None = None


class SellMedianPriceByRoomData(BaseModel):
    room_1: int | None = None
    room_2: int | None = None
    room_3: int | None = None
    room_4: int | None = None
    room_5: int | None = None
    room_6: int | None = None
    room_7: int | None = None


class RentMedianPriceByRoomData(BaseModel):
    room_1: int | None = None
    room_2: int | None = None
    room_3: int | None = None
    room_4: int | None = None
    room_5: int | None = None
    room_6: int | None = None
    room_7: int | None = None


class AppartmentData(BaseModel):
    sell_median_price: SellMedianPriceData
    rent_median_price: RentMedianPriceData
    sell_median_price_by_room: SellMedianPriceByRoomData
    rent_median_price_by_room: RentMedianPriceByRoomData


class HouseData(BaseModel):
    sell_median_price: SellMedianPriceData
    rent_median_price: RentMedianPriceData
    sell_median_price_by_room: SellMedianPriceByRoomData
    rent_median_price_by_room: RentMedianPriceByRoomData

class TownRealEstateData(BaseModel):
    country_id: str | None = None
    region_id: str | None = None
    region_name: str | None = None
    department_id: str | None = None
    department_name: str | None = None
    postal_code: str | None = None
    city_label: str | None = None
    city: str | None = None
    zipcode: str | None = None
    lat: float | None = None
    lng: float | None = None
    source: str | None = None
    provider: str | None = None
    is_shape: bool | None = None
    appartment_data: AppartmentData
    house_data: HouseData
    


