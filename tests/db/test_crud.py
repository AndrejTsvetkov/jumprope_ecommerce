# pylint: disable=too-many-lines
from decimal import Decimal

import pytest

from app.db import crud, models, schemas


# Product stuff
@pytest.mark.usefixtures('product_category')
def test_get_product_category_by_name(db_session):
    product_category = crud.get_product_category_by_name(db_session, name='Скакалки')
    assert product_category.name == 'Скакалки'  # type: ignore


@pytest.mark.usefixtures('product_category')
def test_get_unknown_product_category_by_name(db_session):
    product_category = crud.get_product_category_by_name(
        db_session, name='Неизвестная категория'
    )
    assert product_category is None


@pytest.mark.usefixtures('product_category')
def test_get_product_category_by_id(db_session):
    product_category = crud.get_product_category_by_id(db_session, category_id=1)
    assert product_category.name == 'Скакалки'  # type: ignore


@pytest.mark.usefixtures('product_category')
def test_get_unknown_product_category_by_id(db_session):
    product_category = crud.get_product_category_by_id(db_session, category_id=100)
    assert product_category is None


def test_create_product_category(db_session):
    product_category_schema = schemas.ProductCategoryCreate(
        name='Скакалки', description='Самые лучшие скакалки'
    )
    crud.create_product_category(db_session, product_category_schema)

    created_product_category = (
        db_session.query(models.ProductCategory)
        .filter(models.ProductCategory.name == 'Скакалки')
        .first()
    )

    assert created_product_category is not None
    assert created_product_category.id == 1


@pytest.mark.usefixtures('characteristic')
def test_get_characteristic_by_name(db_session):
    characteristic = crud.get_characteristic_by_name(db_session, name='Длина троса')
    assert characteristic.name == 'Длина троса'  # type: ignore


@pytest.mark.usefixtures('characteristic')
def test_get_unknown_characteristic_by_name(db_session):
    characteristic = crud.get_product_category_by_name(
        db_session, name='Неизвестная характеристика'
    )
    assert characteristic is None


@pytest.mark.usefixtures('characteristic')
def test_get_characteristic_by_id(db_session):
    characteristic = crud.get_characteristic_by_id(db_session, characteristic_id=1)
    assert characteristic.name == 'Длина троса'  # type: ignore


@pytest.mark.usefixtures('characteristic')
def test_get_unknown_characteristic_by_id(db_session):
    characteristic = crud.get_characteristic_by_id(db_session, characteristic_id=200)
    assert characteristic is None


def test_create_characteristic(db_session):
    characteristic_schema = schemas.CharacteristicCreate(name='Цвет ручек')
    crud.create_characteristic(db_session, characteristic_schema)

    created_characteristic = (
        db_session.query(models.Characteristic)
        .filter(models.Characteristic.name == 'Цвет ручек')
        .first()
    )

    assert created_characteristic is not None
    assert created_characteristic.id == 1


@pytest.mark.usefixtures('product_category')
def test_create_product(db_session):
    product_schema = schemas.ProductWithCategory(
        name='Скоростная скакалка',
        sku='ABC123',
        description='Прыгай как Тайсон!',
        price=1399.00,
        category_id=1,
    )
    crud.create_product(db_session, product_schema)

    created_product = (
        db_session.query(models.Product)
        .filter(models.Product.name == 'Скоростная скакалка')
        .first()
    )

    assert created_product is not None
    assert created_product.id == 1
    assert created_product.category.name == 'Скакалки'


@pytest.mark.usefixtures('product')
def test_get_product_by_id(db_session):
    product = crud.get_product_by_id(db_session, product_id=1)
    assert product.name == 'Скоростная скакалка'  # type: ignore


@pytest.mark.usefixtures('product')
def test_get_unknown_product_by_id(db_session):
    product = crud.get_product_by_id(db_session, product_id=100)
    assert product is None


@pytest.mark.usefixtures('product')
def test_get_product_by_sku(db_session):
    product = crud.get_product_by_sku(db_session, product_sku='ABC123')
    assert product.name == 'Скоростная скакалка'  # type: ignore


@pytest.mark.usefixtures('product')
def test_get_unknown_product_by_sku(db_session):
    product = crud.get_product_by_sku(db_session, product_sku='LolKek')
    assert product is None


@pytest.mark.usefixtures('characteristic', 'product')
def test_add_product_characteristic(db_session):
    product_characteristic_schema = schemas.ProductCharacteristic(
        characteristic_id=1,
        characteristic_value='3 м.',
    )
    crud.add_product_characteristic(
        db_session, product_characteristic_schema, product_id=1
    )

    created_product_characteristic = (
        db_session.query(models.ProductCharacteristic)
        .filter(models.ProductCharacteristic.id == 1)
        .first()
    )
    assert created_product_characteristic is not None
    assert created_product_characteristic.characteristic.name == 'Длина троса'
    assert created_product_characteristic.product.name == 'Скоростная скакалка'


@pytest.mark.parametrize(
    ('filter_by_name', 'filter_by_category_name', 'result'),
    [
        ('ростная скакалка', None, 2),
        ('qwe', None, 0),
        ('', 'Массажёры', 1),
    ],
    ids=[
        'two_products_fit',
        'do_not_fit_any_product',
        'one_product_fit',
    ],
)
@pytest.mark.usefixtures('products')
def test_get_filtered_products_query(
    db_session, filter_by_name, filter_by_category_name, result
):
    movie_filters = schemas.ProductFilters(
        filter_by_name=filter_by_name, filter_by_category_name=filter_by_category_name
    )
    query = crud.get_filtered_products_query(db_session, movie_filters)

    assert len(query.all()) == result


@pytest.mark.parametrize(
    ('sort_by_price', 'first_product_name'),
    [
        (True, 'Самая скоростная скакалка'),
        (False, 'Скоростная скакалка'),
    ],
)
@pytest.mark.usefixtures('products')
def test_get_filtered_products_query_price(
    db_session, sort_by_price, first_product_name
):
    product_filters = schemas.ProductFilters(sort_by_price=sort_by_price)
    query = crud.get_filtered_products_query(db_session, product_filters)

    product_list = query.all()
    assert product_list[0].name == first_product_name


# Order stuff
def test_create_order_user(db_session):
    user_schema = schemas.User(
        login='qwertyqwerty@rambler.ru',
        first_name='Иван',
        second_name='Иваныч',
        last_name='Иванов',
        telephone_number='8 (800) 555-35-35',
    )
    crud.create_order_user(db_session, user_schema)

    created_user = (
        db_session.query(models.User)
        .filter(models.User.login == 'qwertyqwerty@rambler.ru')
        .first()
    )

    assert created_user is not None
    assert created_user.id == 1


@pytest.mark.usefixtures('user')
def test_get_user_by_login(db_session):
    user = crud.get_user_by_login(db_session, login='qwertyqwerty@rambler.ru')
    assert user.first_name == 'Иван'  # type: ignore


@pytest.mark.usefixtures('user')
def test_get_unknown_user_by_login(db_session):
    user = crud.get_user_by_login(db_session, login='неизвестный логин')
    assert user is None


def test_create_shipping_address(db_session):
    shipping_address_schema = schemas.ShippingAddress(
        country='Россия',
        city='Тверь',
        postcode='171390',
        address='Мой адрес',
        apartment='кв. 10',
    )
    crud.create_shipping_address(db_session, shipping_address_schema)

    created_address = (
        db_session.query(models.ShippingAddress)
        .filter(models.ShippingAddress.id == 1)
        .first()
    )

    assert created_address is not None
    assert created_address.postcode == '171390'


@pytest.mark.usefixtures('user', 'shipping_address')
def test_create_order(db_session):
    crud.create_order(
        db=db_session,
        total=Decimal('1999.00'),
        is_paid=False,
        user_id=1,
        shipping_address_id=1,
    )

    created_order = db_session.query(models.Order).filter(models.Order.id == 1).first()

    assert created_order is not None
    assert created_order.total == Decimal('1999.00')
    assert created_order.user.login == 'qwertyqwerty@rambler.ru'
    assert created_order.shipping_address.country == 'Россия'


def test_add_order_item(db_session):
    item_schema = schemas.Item(id=1)
    order_item_schema = schemas.OrderItems(
        product=item_schema,
        quantity=7,
        price_per_item=Decimal('1199.00'),
    )
    crud.add_order_item(db_session, order_item_schema, 1)

    created_order_item = (
        db_session.query(models.OrderItems).filter(models.OrderItems.id == 1).first()
    )

    assert created_order_item is not None
    assert created_order_item.quantity == 7


@pytest.mark.usefixtures('user')
def test_update_user_information(db_session):
    new_user_info = schemas.User(
        login='newemail@rambler.ru',
        first_name='Иван',
        second_name='Иваныч',
        last_name='Иванов',
        telephone_number='8 (800) 555-36-36',
    )
    crud.update_user_information(db=db_session, user_id=1, user_info=new_user_info)

    updated_user = db_session.query(models.User).filter(models.User.id == 1).first()
    assert updated_user is not None
    assert updated_user.login == 'newemail@rambler.ru'
    assert updated_user.telephone_number == '8 (800) 555-36-36'


@pytest.mark.usefixtures('order')
def test_get_order_by_id(db_session):
    order = crud.get_order_by_id(db_session, order_id=1)
    assert order.total == Decimal('1000.00')  # type: ignore


@pytest.mark.usefixtures('order')
def test_get_unknown_order_by_id(db_session):
    order = crud.get_order_by_id(db_session, order_id=100)
    assert order is None
