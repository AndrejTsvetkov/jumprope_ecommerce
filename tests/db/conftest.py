# pylint: disable=W0621
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import models


def get_engine(db_file):
    return create_engine(
        f'sqlite:///{db_file}',
        connect_args={'check_same_thread': False},
    )


def get_session(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def create_session(engine):
    session = get_session(engine)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture()
def _init_db():
    db_fd, db_file = tempfile.mkstemp()

    engine = get_engine(db_file)
    models.Base.metadata.create_all(bind=engine)

    with create_session(engine) as local_session:
        yield local_session

    models.Base.metadata.drop_all(bind=engine)
    os.close(db_fd)
    os.unlink(db_file)


@pytest.fixture()
def db_session(_init_db):
    return _init_db


@pytest.fixture()
def product_category(db_session):
    product_category = models.ProductCategory(
        id=1, name='Скакалки', description='Самые лучшие скакалки'
    )
    db_session.add(product_category)
    db_session.commit()


@pytest.fixture()
def characteristic(db_session):
    characteristic = models.Characteristic(id=1, name='Длина троса')
    db_session.add(characteristic)
    db_session.commit()


@pytest.fixture()
def product(db_session):
    product = models.Product(
        id=1,
        name='Скоростная скакалка',
        sku='ABC123',
        description='Прыгай как Тайсон!',
        price=1399.00,
        category_id=1,
    )
    db_session.add(product)
    db_session.commit()


@pytest.mark.usefixtures('product_categories')
@pytest.fixture()
def products(db_session):
    product_category1 = models.ProductCategory(
        id=1, name='Скакалки', description='Самые лучшие скакалки'
    )
    product_category2 = models.ProductCategory(
        id=2, name='Массажёры', description='Самые лучшие массажёры'
    )
    db_session.add(product_category1)
    db_session.add(product_category2)
    product1 = models.Product(
        id=1,
        name='Скоростная скакалка',
        sku='ABC123',
        description='Прыгай как Тайсон!',
        price=1099.00,
        category_id=1,
    )
    product2 = models.Product(
        id=2,
        name='Самая скоростная скакалка',
        sku='DCE123',
        description='Порхай как бабочка, жаль что скоро экзамены...',
        price=1299.00,
        category_id=1,
    )
    product3 = models.Product(
        id=3,
        name='Foam roller',
        sku='FOSAF1',
        description='Хорошо восстанавливает мышцы',
        price=799.00,
        category_id=2,
    )

    db_session.add(product1)
    db_session.add(product2)
    db_session.add(product3)
    db_session.commit()


@pytest.fixture()
def user(db_session):
    user = models.User(
        id=1,
        login='qwertyqwerty@rambler.ru',
        first_name='Иван',
        second_name='Иваныч',
        last_name='Иванов',
        telephone_number='8 (800) 555-35-35',
    )
    db_session.add(user)
    db_session.commit()


@pytest.fixture()
def shipping_address(db_session):
    shipping_address = models.ShippingAddress(
        id=1,
        country='Россия',
        city='Москва',
        postcode='119991',
        address='Мой адрес',
        apartment='кв. 1',
    )
    db_session.add(shipping_address)
    db_session.commit()


@pytest.fixture()
def order(db_session):
    order = models.Order(
        id=1,
        creation_date=datetime.now(),
        total=Decimal('1000.00'),
        is_paid=True,
        is_processed=True,
        user_id=1,
        shipping_address_id=1,
    )
    db_session.add(order)
    db_session.commit()
