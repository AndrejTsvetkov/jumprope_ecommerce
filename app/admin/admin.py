import warnings

from flask import Flask
from flask_admin import Admin

from app.admin.views import (
    CharacteristicView,
    OrderItemView,
    OrderView,
    ProductCategoryView,
    ProductCharacteristicView,
    ProductInventoryView,
    ProductView,
    ShippingAddressView,
    UserView,
)
from app.db import models
from app.db.database import get_session


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = 'very_secret_key'
    admin = Admin(app)

    session = get_session()()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)
        admin.add_view(CharacteristicView(models.Characteristic, session))
        admin.add_view(ProductCharacteristicView(models.ProductCharacteristic, session))
        admin.add_view(ProductCategoryView(models.ProductCategory, session))
        admin.add_view(ProductView(models.Product, session))
        admin.add_view(ProductInventoryView(models.ProductInventory, session))
        admin.add_view(UserView(models.User, session))
        admin.add_view(OrderView(models.Order, session))
        admin.add_view(ShippingAddressView(models.ShippingAddress, session))
        admin.add_view(OrderItemView(models.OrderItems, session))
    return app


if __name__ == '__main__':
    create_app().run()
