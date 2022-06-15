from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import crud, models, schemas
from app.db.schemas import HTTPError
from app.dependencies import get_db
from app.exceptions import (
    CategoryAlreadyRegistered,
    CategoryNotFound,
    CharacteristicAlreadyRegistered,
    CharacteristicNotFound,
    DuplicateCharacteristic,
    ProductAlreadyRegistered,
    ProductNotFound,
    WrongPrice,
)

router = APIRouter(
    prefix='/products',
    tags=['products'],
)


@router.post(
    '/categories',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProductCategory,
    responses={
        CategoryAlreadyRegistered.status_code: {
            'model': HTTPError,
            'description': CategoryAlreadyRegistered.detail,
        },
    },
)
def add_category(
    product_category: schemas.ProductCategoryCreate, db: Session = Depends(get_db)
) -> models.ProductCategory:
    db_product_category = crud.get_product_category_by_name(
        db=db, name=product_category.name
    )
    if db_product_category:
        raise CategoryAlreadyRegistered
    return crud.create_product_category(db=db, product_category=product_category)


@router.post(
    '/characteristic',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Characteristic,
    responses={
        CharacteristicAlreadyRegistered.status_code: {
            'model': HTTPError,
            'description': CharacteristicAlreadyRegistered.detail,
        },
    },
)
def add_characteristic(
    characteristic: schemas.CharacteristicCreate, db: Session = Depends(get_db)
) -> models.Characteristic:
    db_characteristic = crud.get_characteristic_by_name(db=db, name=characteristic.name)
    if db_characteristic:
        raise CharacteristicAlreadyRegistered
    return crud.create_characteristic(db=db, characteristic=characteristic)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProductExt,
    responses={
        CategoryNotFound.status_code: {
            'model': HTTPError,
            'description': CategoryNotFound.detail,
        },
        ProductAlreadyRegistered.status_code: {
            'model': HTTPError,
            'description': ProductAlreadyRegistered.detail,
        },
        CharacteristicNotFound.status_code: {
            'model': HTTPError,
            'description': CharacteristicNotFound.detail,
        },
        DuplicateCharacteristic.status_code: {
            'model': HTTPError,
            'description': DuplicateCharacteristic.detail,
        },
        WrongPrice.status_code: {
            'model': HTTPError,
            'description': WrongPrice.detail,
        },
    },
)
def add_product(
    product: schemas.ProductCreate, db: Session = Depends(get_db)
) -> models.Product:
    db_category = crud.get_product_category_by_id(
        db=db, category_id=product.category_id
    )
    if not db_category:
        raise CategoryNotFound

    # see if there is an object with the same SKU (артикул)
    db_product = crud.get_product_by_sku(db=db, product_sku=product.sku)
    if db_product:
        raise ProductAlreadyRegistered

    product_without_characteristics = schemas.ProductWithCategory(
        name=product.name,
        sku=product.sku,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
    )

    # See if the price more than zero
    try:
        db_product = crud.create_product(db=db, product=product_without_characteristics)
    except IntegrityError as err:
        raise WrongPrice from err

    # Add the specified characteristics
    if product.characteristics:
        add_characteristics(
            db=db, characteristics=product.characteristics, product_id=db_product.id
        )

    return db_product


def add_characteristics(
    db: Session, characteristics: list[schemas.ProductCharacteristic], product_id: int
) -> None:
    for characteristic in characteristics:
        characteristic_db = crud.get_characteristic_by_id(
            db=db, characteristic_id=characteristic.characteristic_id
        )
        if not characteristic_db:
            raise CharacteristicNotFound

        try:
            crud.add_product_characteristic(
                db=db, product_characteristic=characteristic, product_id=product_id
            )
        except IntegrityError as err:
            raise DuplicateCharacteristic from err


@router.get(
    '/{product_id}',
    response_model=schemas.ProductExt,
    responses={
        ProductNotFound.status_code: {
            'model': HTTPError,
            'description': ProductNotFound.detail,
        }
    },
)
def get_product(product_id: int, db: Session = Depends(get_db)) -> models.Product:
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise ProductNotFound
    return db_product


@router.get(  # pragma: no cover  Can't construct query object without db connection
    '/',
    response_model=Page[schemas.ProductExt],
)
def get_products(
    product_filters: schemas.ProductFilters = Depends(), db: Session = Depends(get_db)
) -> AbstractPage[Any]:
    return paginate(crud.get_filtered_products_query(db, product_filters))


@router.patch(
    '/{product_id}/inventory',
    response_model=schemas.ProductInventory,
    responses={
        ProductNotFound.status_code: {
            'model': HTTPError,
            'description': ProductNotFound.detail,
        }
    },
)
def increase_product_quantity(
    product_id: int, inc_value: int, db: Session = Depends(get_db)
) -> models.ProductInventory:
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise ProductNotFound
    db_product.increase_quantity(inc_value)
    return db_product.product_inventory
