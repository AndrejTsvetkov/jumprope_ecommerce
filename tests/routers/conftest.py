# pylint: disable=W0621
from datetime import datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.db import models
from app.main import app


@pytest.fixture(scope='session')
def client():
    test_client = TestClient(app)
    return test_client


@pytest.fixture()
def get_product_category_by_name_mock(mocker):
    return mocker.patch('app.db.crud.get_product_category_by_name')


@pytest.fixture()
def create_product_category_mock(mocker):
    return mocker.patch('app.db.crud.create_product_category')


@pytest.fixture()
def product_category():
    return models.ProductCategory(
        id=1, name='Скакалки', description='Самые лучшие скакалки'
    )


@pytest.fixture()
def get_characteristic_by_name_mock(mocker):
    return mocker.patch('app.db.crud.get_characteristic_by_name')


@pytest.fixture()
def create_characteristic_mock(mocker):
    return mocker.patch('app.db.crud.create_characteristic')


@pytest.fixture()
def characteristic():
    return models.Characteristic(id=1, name='Длина троса')


@pytest.fixture()
def get_product_category_by_id_mock(mocker):
    return mocker.patch('app.db.crud.get_product_category_by_id')


@pytest.fixture()
def get_product_by_sku_mock(mocker):
    return mocker.patch('app.db.crud.get_product_by_sku')


@pytest.fixture()
def get_product_by_id_mock(mocker):
    return mocker.patch('app.db.crud.get_product_by_id')


@pytest.fixture()
def create_product_mock(mocker):
    return mocker.patch('app.db.crud.create_product')


@pytest.fixture()
def get_order_by_id_mock(mocker):
    return mocker.patch('app.db.crud.get_order_by_id')


@pytest.fixture()
def add_product_json():
    return {
        'name': 'Бисерная скакалка',
        'sku': '123',
        'description': 'Лучшая скакалка в мире',
        'price': 1399.0,
        'category_id': 1,
        'characteristics': [{'characteristic_id': 1, 'characteristic_value': '3 м.'}],
    }


@pytest.fixture()
def product():
    product = models.Product(
        id=1,
        name='Бисерная скакалка',
        sku='ABC123',
        description='qwerty',
        price=Decimal('1000.0'),
    )
    product.product_inventory = models.ProductInventory(id=1, product_id=1, quantity=3)
    return product


@pytest.fixture()
def user():
    user = models.User(
        id=1,
        login='qwertyqwerty@rambler.ru',
        first_name='Иван',
        second_name='Иваныч',
        last_name='Иванов',
        telephone_number='8 (800) 555-35-35',
    )
    return user


@pytest.fixture()
def shipping_address():
    shipping_address = models.ShippingAddress(
        id=1,
        country='Россия',
        city='Москва',
        postcode='119991',
        address='Мой адрес',
        apartment='кв. 1',
    )
    return shipping_address


@pytest.fixture()
def order(user, shipping_address):
    return models.Order(
        id=1,
        creation_date=datetime.now(),
        total=Decimal('1000.00'),
        is_paid=0,
        is_processed=0,
        user_id=1,
        shipping_address_id=1,
        user=user,
        shipping_address=shipping_address,
    )
