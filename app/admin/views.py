from flask_admin.contrib.sqla import ModelView


class CharacteristicView(ModelView):
    can_delete = False

    form_create_rules = ['name']
    form_edit_rules = ['name']


class ProductCharacteristicView(ModelView):
    can_delete = False


class ProductCategoryView(ModelView):
    can_delete = False

    form_create_rules = ['name', 'description']
    form_edit_rules = ['name', 'description']


class ProductView(ModelView):
    can_delete = False

    form_excluded_columns = ['product_in_orders', 'characteristics']


class ProductInventoryView(ModelView):
    can_delete = False


class UserView(ModelView):
    can_delete = False
    can_create = False

    form_excluded_columns = ['orders']


class OrderView(ModelView):
    can_delete = False
    can_create = False
    can_edit = False


class ShippingAddressView(ModelView):
    can_delete = False
    can_create = False

    form_excluded_columns = ['orders']


class OrderItemView(ModelView):
    can_delete = False
    can_create = False
    can_edit = False
