from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.database import Base


# User tables
class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    # here we store email (login=email)
    login = sa.Column(sa.String, unique=True, nullable=False)
    first_name = sa.Column(sa.String, nullable=False)
    second_name = sa.Column(sa.String, nullable=True)
    last_name = sa.Column(sa.String, nullable=False)
    telephone_number = sa.Column(sa.String, nullable=True)

    # for future modifications
    is_registered = sa.Column(sa.Boolean, default=False, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=True)

    orders = relationship('Order', back_populates='user', uselist=True)

    def __repr__(self) -> str:
        return f'<User "{self.login}">'


# Product tables
class ProductCategory(Base):
    __tablename__ = 'product_category'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False)

    products = relationship('Product', back_populates='category', uselist=True)

    def __repr__(self) -> str:
        return f'<Category "{self.name}">'


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = (sa.CheckConstraint('price > 0'),)

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, nullable=False)
    # SKU - stock keeping unit (артикул, идентификатор товарной позиции)
    sku = sa.Column(sa.String, unique=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    price = sa.Column(sa.Numeric(10, 8), nullable=False)
    category_id = sa.Column(sa.Integer, sa.ForeignKey(ProductCategory.id))

    category = relationship('ProductCategory', back_populates='products', uselist=False)
    characteristics = relationship(
        'ProductCharacteristic', back_populates='product', uselist=True
    )
    # (Product, Inventory) - one to one relationship
    product_inventory = relationship(
        'ProductInventory', back_populates='product', uselist=False
    )
    product_in_orders = relationship(
        'OrderItems', back_populates='product', uselist=True
    )

    def increase_quantity(self, inc_value: int) -> None:
        self.product_inventory.quantity += inc_value

    def decrease_quantity(self, dec_value: int) -> None:
        self.product_inventory.quantity -= dec_value

    def __repr__(self) -> str:
        return f'<Product "{self.name}", SKU="{self.sku}">'


class ProductInventory(Base):
    __tablename__ = 'product_inventory'
    __table_args__ = (sa.CheckConstraint('quantity >= 0'),)

    id = sa.Column(sa.Integer, primary_key=True)
    product_id = sa.Column(sa.Integer, sa.ForeignKey(Product.id))
    quantity = sa.Column(sa.Integer, default=0, nullable=False)

    # (Product, Inventory)  - one to one relationship
    product = relationship('Product', back_populates='product_inventory')

    def __repr__(self) -> str:
        return f'<{self.product}, quantity="{self.quantity}">'


class Characteristic(Base):
    __tablename__ = 'characteristic'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, unique=True, nullable=False)

    characteristic_values = relationship(
        'ProductCharacteristic', back_populates='characteristic', uselist=True
    )

    def __repr__(self) -> str:
        return f'<Characteristic "{self.name}">'


class ProductCharacteristic(Base):
    __tablename__ = 'product_characteristic'
    # One product cannot have several identical characteristics
    __table_args__ = (
        sa.UniqueConstraint(
            'product_id', 'characteristic_id', name='_product_characteristic_uc'
        ),
    )

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    product_id = sa.Column(sa.Integer, sa.ForeignKey(Product.id))
    characteristic_id = sa.Column(sa.Integer, sa.ForeignKey(Characteristic.id))
    characteristic_value = sa.Column(sa.String, nullable=False)

    characteristic = relationship(
        'Characteristic', back_populates='characteristic_values', uselist=False
    )
    product = relationship('Product', back_populates='characteristics', uselist=False)


# Order tables
class ShippingAddress(Base):
    __tablename__ = 'shipping_address'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    country = sa.Column(sa.String, nullable=False)
    city = sa.Column(sa.String, nullable=False)
    postcode = sa.Column(sa.String, nullable=False)
    address = sa.Column(sa.String, nullable=False)
    apartment = sa.Column(sa.String, nullable=True)

    orders = relationship('Order', back_populates='shipping_address', uselist=True)

    def __repr__(self) -> str:
        return f'<Address "{self.city}, {self.address}, {self.apartment}">'


class Order(Base):
    __tablename__ = 'order'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    creation_date = sa.Column(sa.DateTime(), default=datetime.now(), nullable=False)
    total = sa.Column(sa.Numeric(10, 8), nullable=False)
    is_paid = sa.Column(sa.Boolean, nullable=False)
    is_processed = sa.Column(sa.Boolean, default=False, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    shipping_address_id = sa.Column(sa.Integer, sa.ForeignKey(ShippingAddress.id))

    user = relationship('User', back_populates='orders', uselist=False)
    items = relationship('OrderItems', back_populates='order', uselist=True)
    shipping_address = relationship(
        'ShippingAddress', back_populates='orders', uselist=False
    )

    def complete(self) -> None:
        self.is_processed = True

    def __repr__(self) -> str:
        order_date = self.creation_date.strftime('%b %d %Y %H:%M:%S')
        return f'<Order by {self.user.login} from {order_date}>'


class OrderItems(Base):
    __tablename__ = 'order_items'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    quantity = sa.Column(sa.Integer, nullable=False)
    price_per_item = sa.Column(sa.Numeric(10, 8), nullable=False)
    order_id = sa.Column(sa.Integer, sa.ForeignKey(Order.id))
    product_id = sa.Column(sa.Integer, sa.ForeignKey(Product.id))

    order = relationship('Order', back_populates='items', uselist=False)
    product = relationship('Product', back_populates='product_in_orders', uselist=False)
