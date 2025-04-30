from repository.user_repo import get_user, save_user
from utils.string_utils import hash_password


def register_user(user_id: int, name: str, password: str, balance=0.0):
    from model.user import User

    if balance < 0:
        raise ValueError("Balance cannot be negative")

    existing_user = get_user(user_id)
    if existing_user:
        balance = existing_user.balance

    hashed = hash_password(password)
    user = User(id=user_id, name=name, balance=balance)
    user.hashed_password = hashed
    save_user(user)
    return user


def authenticate(user_id: int, password: str):
    user = get_user(user_id)
    if not user:
        return False
    return user.hashed_password == hash_password(password)
