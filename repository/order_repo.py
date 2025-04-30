from model.order import Order

_order_store = []


def save_order(order: Order):
    _order_store.append(order)
    return True


def list_orders_for_user(user_id: int):
    return [o for o in _order_store if o.user_id == user_id]
