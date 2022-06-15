from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Query, Session

from app.db import models, schemas


# Product stuff
def get_product_category_by_name(
    db: Session, name: str
) -> Optional[models.ProductCategory]:
    return (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.name == name)
        .first()
    )


def get_product_category_by_id(
    db: Session, category_id: int
) -> Optional[models.ProductCategory]:
    return (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.id == category_id)
        .first()
    )


def create_product_category(
    db: Session, product_category: schemas.ProductCategoryCreate
) -> models.ProductCategory:
    db_product_category = models.ProductCategory(**product_category.dict())
    db.add(db_product_category)
    db.flush()
    return db_product_category


def get_characteristic_by_name(
    db: Session, name: str
) -> Optional[models.Characteristic]:
    return (
        db.query(models.Characteristic)
        .filter(models.Characteristic.name == name)
        .first()
    )


def get_characteristic_by_id(
    db: Session, characteristic_id: int
) -> Optional[models.Characteristic]:
    return (
        db.query(models.Characteristic)
        .filter(models.Characteristic.id == characteristic_id)
        .first()
    )


def create_characteristic(
    db: Session, characteristic: schemas.CharacteristicCreate
) -> models.Characteristic:
    db_characteristic = models.Characteristic(**characteristic.dict())
    db.add(db_characteristic)
    db.flush()
    return db_characteristic


def create_product(db: Session, product: schemas.ProductWithCategory) -> models.Product:
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.flush()
    db_product_inventory = models.ProductInventory(product_id=db_product.id)
    db.add(db_product_inventory)
    return db_product


def get_product_by_id(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_sku(db: Session, product_sku: str) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.sku == product_sku).first()


def add_product_characteristic(
    db: Session, product_characteristic: schemas.ProductCharacteristic, product_id: int
) -> None:
    db_product_characteristic = models.ProductCharacteristic(
        **product_characteristic.dict(), product_id=product_id
    )
    db.add(db_product_characteristic)
    db.flush()


def get_filtered_products_query(
    db: Session, product_filters: schemas.ProductFilters
) -> Query:
    filters = []
    if product_filters.filter_by_name:
        filters.append(models.Product.name.contains(product_filters.filter_by_name))
    if product_filters.filter_by_category_name:
        filters.append(
            models.Product.category.has(
                models.ProductCategory.name == product_filters.filter_by_category_name
            )
        )
    products_query = db.query(models.Product).filter(*filters)
    if product_filters.sort_by_price:
        products_query = products_query.order_by(models.Product.price.desc())

    return products_query


# Order stuff
def create_order_user(db: Session, order_user: schemas.User) -> models.User:
    db_order_user = models.User(**order_user.dict())
    db.add(db_order_user)
    db.flush()
    return db_order_user


def get_user_by_login(db: Session, login: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.login == login).first()


def update_user_information(db: Session, user_id: int, user_info: schemas.User) -> None:
    db.query(models.User).filter(models.User.id == user_id).update(user_info.dict())


def create_shipping_address(
    db: Session, shipping_address: schemas.ShippingAddress
) -> models.ShippingAddress:
    db_shipping_address = models.ShippingAddress(**shipping_address.dict())
    db.add(db_shipping_address)
    db.flush()
    return db_shipping_address


def create_order(
    db: Session, total: Decimal, is_paid: bool, user_id: int, shipping_address_id: int
) -> models.Order:
    db_order = models.Order(
        total=total,
        is_paid=is_paid,
        user_id=user_id,
        shipping_address_id=shipping_address_id,
    )
    db.add(db_order)
    db.flush()
    return db_order


def add_order_item(db: Session, order_item: schemas.OrderItems, order_id: int) -> None:
    db_order_items = models.OrderItems(
        quantity=order_item.quantity,
        price_per_item=order_item.price_per_item,
        product_id=order_item.product.id,
        order_id=order_id,
    )
    db.add(db_order_items)
    db.flush()


def get_order_by_id(db: Session, order_id: int) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.id == order_id).first()
