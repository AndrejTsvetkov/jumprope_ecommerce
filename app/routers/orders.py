import random

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import crud, models, schemas
from app.db.schemas import HTTPError
from app.dependencies import get_db
from app.exceptions import (
    InsufficientStock,
    OrderAlreadyCompleted,
    OrderNotFound,
    OrderNotPaid,
)

router = APIRouter(
    prefix='/orders',
    tags=['orders'],
)


# So far dummy function that returns the payment status (80% - probability of success)
def pay_order() -> bool:
    if random.random() > 0.8:
        return False
    return True


@router.post(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Order,
    responses={
        InsufficientStock.status_code: {
            'model': HTTPError,
            'description': InsufficientStock.detail,
        },
    },
)
def create_order(order: schemas.Order, db: Session = Depends(get_db)) -> models.Order:
    # check if there's already record about this user
    db_user = crud.get_user_by_login(db=db, login=order.user.login)
    if db_user:
        db_user_info = schemas.User.from_orm(db_user)
        # if the user has specified new info update it
        if db_user_info != order.user.dict():
            crud.update_user_information(
                db=db, user_id=db_user.id, user_info=order.user
            )
    else:
        # otherwise, just create a new record
        db_user = crud.create_order_user(db=db, order_user=order.user)

    # create shipping address
    db_shipping_address = crud.create_shipping_address(
        db=db, shipping_address=order.shipping_address
    )

    # payment emulation
    is_paid = pay_order()

    # create order
    db_order = crud.create_order(
        db=db,
        total=order.total,
        is_paid=is_paid,
        user_id=db_user.id,
        shipping_address_id=db_shipping_address.id,
    )

    # add items in order (their ids are correct by default)
    for item in order.items:
        db_product = crud.get_product_by_id(db=db, product_id=item.product.id)
        # check if there's enough items in stock
        if db_product.product_inventory.quantity < item.quantity:  # type: ignore
            raise InsufficientStock
        db_product.decrease_quantity(item.quantity)  # type: ignore
        crud.add_order_item(db=db, order_item=item, order_id=db_order.id)

    return db_order


@router.patch(
    '/{order_id}',
    response_model=schemas.ProcessedOrder,
    responses={
        OrderNotFound.status_code: {
            'model': HTTPError,
            'description': OrderNotFound.detail,
        },
        OrderNotPaid.status_code: {
            'model': HTTPError,
            'description': OrderNotFound.detail,
        },
        OrderAlreadyCompleted.status_code: {
            'model': HTTPError,
            'description': OrderAlreadyCompleted.detail,
        },
    },
)
def complete_order(
    order_id: int, db: Session = Depends(get_db)
) -> models.ProductInventory:
    db_order = crud.get_order_by_id(db, order_id=order_id)
    if not db_order:
        raise OrderNotFound

    if db_order.is_processed:
        raise OrderAlreadyCompleted

    if not db_order.is_paid:
        raise OrderNotPaid

    db_order.complete()
    return db_order
