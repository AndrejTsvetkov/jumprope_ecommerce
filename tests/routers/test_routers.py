from http import HTTPStatus

from sqlalchemy.exc import IntegrityError

from app.exceptions import (
    CategoryAlreadyRegistered,
    CategoryNotFound,
    CharacteristicAlreadyRegistered,
    OrderAlreadyCompleted,
    OrderNotFound,
    OrderNotPaid,
    ProductAlreadyRegistered,
    ProductNotFound,
    WrongPrice,
)


def test_add_category(
    client,
    get_product_category_by_name_mock,
    create_product_category_mock,
    product_category,
):
    get_product_category_by_name_mock.return_value = None
    create_product_category_mock.return_value = product_category

    response = client.post(
        '/api/products/categories',
        json={
            'name': 'Скакалки',
            'description': 'Самые лучшие скакалки',
        },
    )

    assert response.status_code == HTTPStatus.CREATED, response.text
    data = response.json()
    assert data['name'] == 'Скакалки'


def test_add_category_failed(client, get_product_category_by_name_mock):
    get_product_category_by_name_mock.return_value = 'fake_category'

    response = client.post(
        '/api/products/categories',
        json={
            'name': 'Скакалки',
            'description': 'Самые лучшие скакалки',
        },
    )

    assert response.status_code == CategoryAlreadyRegistered.status_code, response.text
    data = response.json()
    assert data['detail'] == CategoryAlreadyRegistered.detail


def test_add_characteristic(
    client, get_characteristic_by_name_mock, create_characteristic_mock, characteristic
):
    get_characteristic_by_name_mock.return_value = None
    create_characteristic_mock.return_value = characteristic

    response = client.post(
        '/api/products/characteristic',
        json={
            'name': 'Длина троса',
        },
    )

    assert response.status_code == HTTPStatus.CREATED, response.text
    data = response.json()
    assert data['name'] == 'Длина троса'


def test_add_characteristic_failed(client, get_characteristic_by_name_mock):
    get_characteristic_by_name_mock.return_value = 'fake_characteristic'

    response = client.post(
        '/api/products/characteristic',
        json={
            'name': 'Длина троса',
        },
    )

    assert (
        response.status_code == CharacteristicAlreadyRegistered.status_code
    ), response.text
    data = response.json()
    assert data['detail'] == CharacteristicAlreadyRegistered.detail


def test_add_product_not_category(
    client, get_product_category_by_id_mock, add_product_json
):
    get_product_category_by_id_mock.return_value = None

    response = client.post('/api/products/', json=add_product_json)

    assert response.status_code == CategoryNotFound.status_code, response.text
    data = response.json()
    assert data['detail'] == CategoryNotFound.detail


def test_add_existing_product(
    client, get_product_by_sku_mock, get_product_category_by_id_mock, add_product_json
):
    get_product_category_by_id_mock.return_value = 'fake_category'
    get_product_by_sku_mock.return_value = 'fake_product'

    response = client.post('/api/products/', json=add_product_json)

    assert response.status_code == ProductAlreadyRegistered.status_code, response.text
    data = response.json()
    assert data['detail'] == ProductAlreadyRegistered.detail


def test_add_product_wrong_price(
    client,
    get_product_by_sku_mock,
    get_product_category_by_id_mock,
    create_product_mock,
    add_product_json,
):
    get_product_category_by_id_mock.return_value = 'fake_category'
    get_product_by_sku_mock.return_value = None
    create_product_mock.side_effect = IntegrityError('Mock', 'Mock', 'Mock')

    response = client.post('/api/products/', json=add_product_json)

    assert response.status_code == WrongPrice.status_code, response.text
    data = response.json()
    assert data['detail'] == WrongPrice.detail


def test_get_product_failed(client, get_product_by_id_mock):
    get_product_by_id_mock.return_value = None

    response = client.get('/api/products/1')

    assert response.status_code == ProductNotFound.status_code, response.text
    data = response.json()
    assert data['detail'] == ProductNotFound.detail


def test_increase_product_quantity(client, get_product_by_id_mock, product):
    get_product_by_id_mock.return_value = product

    response = client.patch('/api/products/1/inventory', params={'inc_value': 4})

    assert response.status_code == HTTPStatus.OK, response.text
    data = response.json()
    assert data['quantity'] == 7


def test_increase_product_quantity_failed(client, get_product_by_id_mock):
    get_product_by_id_mock.return_value = None

    response = client.patch('/api/products/1/inventory', params={'inc_value': 4})

    assert response.status_code == ProductNotFound.status_code, response.text
    data = response.json()
    assert data['detail'] == ProductNotFound.detail


def test_complete_order_not_order(client, get_order_by_id_mock):
    get_order_by_id_mock.return_value = None

    response = client.patch('/api/orders/1')

    assert response.status_code == OrderNotFound.status_code, response.text
    data = response.json()
    assert data['detail'] == OrderNotFound.detail


def test_complete_order_processed(client, get_order_by_id_mock, order):
    order.is_processed = True
    get_order_by_id_mock.return_value = order

    response = client.patch('/api/orders/1')

    assert response.status_code == OrderAlreadyCompleted.status_code, response.text
    data = response.json()
    assert data['detail'] == OrderAlreadyCompleted.detail


def test_complete_order_not_paid(client, get_order_by_id_mock, order):
    get_order_by_id_mock.return_value = order

    response = client.patch('/api/orders/1')

    assert response.status_code == OrderNotPaid.status_code, response.text
    data = response.json()
    assert data['detail'] == OrderNotPaid.detail


def test_complete_order(client, get_order_by_id_mock, order):
    order.is_paid = True
    get_order_by_id_mock.return_value = order

    response = client.patch('/api/orders/1')

    assert response.status_code == HTTPStatus.OK, response.text
    data = response.json()
    assert data['is_processed'] == 1
