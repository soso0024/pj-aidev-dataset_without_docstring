import random
from model.user import User
from model.order import Order


def generate_users(n):
    if n < 0:
        raise ValueError("Number of users must be positive")

    users = []
    for i in range(1, n + 1):
        users.append(User(id=i, name=f"User{i}", balance=random.uniform(10, 100)))
    return users


def generate_orders(users, max_orders=3):
    orders = []
    print("\nGenerating orders...")
    for user in users:
        available_balance = user.balance
        for _ in range(random.randint(1, max_orders)):
            if available_balance <= 1:
                print("Skipping order generation due to insufficient balance.")
                break
            amount = random.uniform(1, min(available_balance, user.balance))
            order = Order(user_id=user.id, amount=amount)
            orders.append(order)
            available_balance -= amount
    return orders
