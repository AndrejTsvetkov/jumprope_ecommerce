from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Product category schemas
class ProductCategoryBase(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategory(ProductCategoryBase):
    id: int


# Characteristic schemas
class CharacteristicBase(BaseModel):
    name: str


class CharacteristicCreate(CharacteristicBase):
    pass


class Characteristic(CharacteristicBase):
    id: int

    class Config:
        orm_mode = True


# Product characteristics schemas
class ProductCharacteristic(BaseModel):
    characteristic_id: int
    characteristic_value: str

    class Config:
        orm_mode = True


class ProductCharacteristicExt(BaseModel):
    characteristic_value: str
    characteristic: Optional[Characteristic]

    class Config:
        orm_mode = True


# Product schemas
class ProductBase(BaseModel):
    name: str
    sku: str
    description: str
    price: Decimal

    class Config:
        orm_mode = True


class ProductWithCategory(ProductBase):
    category_id: int


class ProductCreate(ProductWithCategory):
    characteristics: Optional[list[ProductCharacteristic]]


class Product(ProductCreate):
    id: int


class ProductExt(ProductBase):
    id: int
    category: ProductCategory
    characteristics: Optional[list[ProductCharacteristicExt]]


class ProductFilters(BaseModel):
    filter_by_name: Optional[str] = ''
    sort_by_price: Optional[bool] = False
    filter_by_category_name: Optional[str]


# Product inventory schemas
class ProductInventory(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


# User schemas
class User(BaseModel):
    # login = email
    login: str
    first_name: str
    second_name: Optional[str]
    last_name: str
    telephone_number: Optional[str]

    class Config:
        orm_mode = True


# Order schemas
class Item(BaseModel):
    id: int

    class Config:
        orm_mode = True


class OrderItems(BaseModel):
    product: Item
    quantity: int
    price_per_item: Decimal

    class Config:
        orm_mode = True


class ShippingAddress(BaseModel):
    country: str
    city: str
    postcode: str
    address: str
    apartment: Optional[str]

    class Config:
        orm_mode = True


class Order(BaseModel):
    total: Decimal
    user: User
    shipping_address: ShippingAddress
    items: list[OrderItems]

    class Config:
        orm_mode = True


class ProcessedOrder(Order):
    is_processed: bool


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            'example': {'detail': 'HTTP Exception'},
        }
