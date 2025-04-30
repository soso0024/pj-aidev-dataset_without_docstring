from repository.user_repo import get_user, save_user
from repository.order_repo import save_order
from model.order import Order


def make_payment(user_id: int, amount: float):
    if amount <= 0:
        raise ValueError("Payment amount must be positive")

    user = get_user(user_id)
    if not user:
        raise ValueError("User not found")
    new_balance = user.debit(amount)
    order = Order(user_id=user_id, amount=amount)
    save_order(order)
    save_user(user)
    return new_balance
